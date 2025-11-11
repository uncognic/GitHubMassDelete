from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QLabel, QMainWindow, QWidget
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from github import Github, Auth
import sys

class GitHubMassDelete(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GitHub Mass Delete")
        self.resize(600, 400)
        
        self.github = None
        self.repos = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        tokenRow = QHBoxLayout()
        self.tokenInput = QLineEdit()
        self.tokenInput.setEchoMode(QLineEdit.Password)
        self.tokenInput.setPlaceholderText("Enter your GitHub token")
        loadButton = QPushButton("Load Repos")
        loadButton.clicked.connect(self.loadRepos)
        tokenRow.addWidget(self.tokenInput)
        tokenRow.addWidget(loadButton)
        layout.addLayout(tokenRow)

        self.repoList = QListWidget()
        self.repoList.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(QLabel("Select repositories to delete:"))
        layout.addWidget(self.repoList)

        deleteButton = QPushButton("Delete Selected Repos")
        deleteButton.clicked.connect(self.deleteSelected)
        layout.addWidget(deleteButton)

        menu = self.menuBar()
        fileMenu = menu.addMenu("File")
        optionsMenu = menu.addMenu("Options")

        self.Quit = QAction("Quit", self)
        self.Quit.triggered.connect(quit)
        fileMenu.addAction(self.Quit)

        self.showOrgAction = QAction("Show organization repositories", self)
        self.showOrgAction.setCheckable(True)
        self.showOrgAction.setChecked(False)
        self.showOrgAction.triggered.connect(self.toggleShowOrg)
        optionsMenu.addAction(self.showOrgAction)

    def toggleShowOrg(self, checked):
        self.showOrgRepos = checked
        if self.repos:
            self.populateRepoList()

    def populateRepoList(self):
        self.repoList.clear()
        for r in self.repos:
            if not self.showOrgRepos and r.owner.type == "Organization":
                continue
            
            flags = []
            if r.private: flags.append("private")
            if r.archived: flags.append("archived")
            if r.fork: flags.append("fork")
            flagStr = f" ({', '.join(flags)})" if flags else ""
            item = QListWidgetItem(f"{r.full_name}{flagStr}")
            item.setData(Qt.UserRole, r)
            self.repoList.addItem(item)
        
    
    def loadRepos(self):
        token = self.tokenInput.text().strip()
        if not token:
            QMessageBox.warning(self, "Error", "Token is required")
            return
        try:
            auth = Auth.Token(token)
            self.github = Github(auth=auth)
            user = self.github.get_user()
            allRepos = list(user.get_repos())
            self.repos = [r for r in allRepos if getattr(r.owner, "login", None) == user.login
                          or r.owner.type == "Organization"]

            self.populateRepoList()

            QMessageBox.information(self, "Done", f"Loaded {len(self.repos)} repositories.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def deleteSelected(self):
        selectedItems = self.repoList.selectedItems()
        if not selectedItems:
            QMessageBox.warning(self, "Warning", "No repositories selected")
            return
        
        confirm = QMessageBox.question(
            self,
            "Confirmation",
            f"Are you SURE that you want to delete {len(selectedItems)} repositories? This action is IRREVERSIBLE!",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return
        
        for item in selectedItems:
            repo = item.data(Qt.UserRole)
            try:
                repo.delete()
                self.repoList.takeItem(self.repoList.row(item))
                print(f"Deleted {repo.full_name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete {repo.full_name}:\n{e}")

        QMessageBox.information(self, "Finished", "Deletion complete")
        self.github.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitHubMassDelete()
    window.show()
    sys.exit(app.exec())



