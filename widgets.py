# This file contains all widget setting
# like buttons and their icons and callbacks
# and Dialogs

from datetime import date
from decimal import Decimal
from PyQt5 import QtWidgets, QtCore, QtGui
import qtawesome as qta

# from uis.h_article import Ui_articleDialog
from uis.h_operations_dialog import Ui_Dialog
import utils
from logger import logger

# ---- Global Var ---- #
NEW_COLOR = "#1dd1a1"
SAVE_COLOR = '#17c0eb'
TRASH_COLOR = '#f77861'
WHITE_COLOR = "#FFFFFF"
# SAVE_COLOR = '#0097e6'

today = date.today()
product_fields = ['art_id', 'code', 'designation', 'ref', 'emp', 'umesure', 'qte', 'prix', 'valeur']
product_headers = ['ID', 'Code', 'Designation', 'Reference', 'EMP', 'UM', 'Qte', 'Prix', 'Valeur']

user_fields = [
    'auth_user.id', 'IFNULL(DATE(last_login), "")', 'username', 'email', 'first_name', 'last_name',
    'p.poste_travaille', 'p.groupe', 'DATE(date_joined)',
]


def interface_callbacks(root):
    """
    Setup all the callbacks and Menus for the main interface.
    """
    buttons = [
        # --- MENUS
        (root.ui.toggleMenuButton, False, lambda: root.toggle_menu()),
        (root.ui.toggleLeftBox, False, lambda: root.toggle_left_box()),     # -- Toggle left box
        (root.ui.extraCloseColumnBtn, False, root.toggle_left_box),         # -- Toggle extra column
        (root.ui.buttonExitPage, False, root.close),

        # -- MAGASIN PAGE --
        (
            root.ui.buttonMagasinPage,
            qta.icon('ri.parking-box-fill', color='#ffffff'),
            lambda: root.goto_page('Magasin')
        ),
        (root.ui.pushButtonSearch, qta.icon('ri.search-line', color=WHITE_COLOR), root.search_article,),  # -- Search Article
        (root.ui.newCatBtn, qta.icon('ri.add-fill', color=NEW_COLOR), root.new_category),              # -- New Category
        (root.ui.newArticleBtn, qta.icon('ri.add-fill', color=NEW_COLOR), root.new_article),           # -- New Article
        (root.ui.editArticleBtn, qta.icon('mdi.clipboard-edit', color="#25CCF7"), root.edit_article),  # -- Edit Article
        (root.ui.newEntryBtn, qta.icon('ri.login-circle-line', color="#44e37b"), root.article_new_entry),  # -- New Entree
        (root.ui.newSortieBtn, qta.icon('ri.logout-circle-r-line', color="#ee4"), root.article_new_sortie),  # --Sortie Article
        (root.ui.delArticleBtn, qta.icon('msc.trashcan', color=TRASH_COLOR), root.delete_article),    # -- Delete Article
        (root.ui.movArticleBtn, qta.icon('ri.arrow-left-right-line', color=WHITE_COLOR), False),    # -- Movement Article

        # --- USERS PAGE ---
        (
            root.ui.buttonUsersPage,
            False,
            lambda: root.goto_page(page='Users')
        ),
        (root.ui.btnSearchUsers, qta.icon('ri.search-line', color=WHITE_COLOR), root.search_users),  # -- Search Article
        (root.ui.newUserBtn, qta.icon('ri.user-add-line', color=NEW_COLOR), root.new_user),            # -- New User --
        (root.ui.editUserBtn, qta.icon('ri.user-settings-line', color='#0097e6'), root.edit_user),      # -- Edit User --
        (root.ui.changePasswordBtn, qta.icon('ri.lock-password-line', color=NEW_COLOR), root.change_password),  # Change Passwd
        (root.ui.delUserBtn, qta.icon('ri.user-unfollow-line', color=TRASH_COLOR), root.delete_user),     # -- Delete User --

        # --- MOVEMENT PAGE ---
        (
            root.ui.buttonMovementPage,
            qta.icon('ri.arrow-left-right-line', color=WHITE_COLOR),
            lambda: root.goto_page('Movements')
        ),
        (root.ui.pushButtonSearchMov, qta.icon('ri.search-line', color=WHITE_COLOR), root.search_movements,),
        (root.ui.btnMovementRefresh, qta.icon('mdi6.refresh', color=WHITE_COLOR), lambda: root.goto_page('Movements')),
        (root.ui.buttonCloseMsgsFrame, False, lambda: root.close_msgs_frame(close=True)),

        # -- COMMANDE PAGE
        (
            root.ui.buttonCommandePage,
            # False,
            qta.icon('mdi6.truck-flatbed', color='#ffffff'),
            lambda: root.goto_page('Commande')
        ),
        (root.ui.newCommandBtn, qta.icon('mdi6.truck-plus', color="#EE5A24"), root.new_commande),   # New Commande
        # Active Commande
        (root.ui.activeCommandBtn, qta.icon('mdi.truck-check', color=NEW_COLOR), root.activate_command),
        (root.ui.delCommandBtn, qta.icon('msc.trashcan', color=TRASH_COLOR), root.delete_commande),    # Delete Commande

        # -- HISTORY PAGE
        (
            root.ui.buttonHistoryPage,
            False,
            # qta.icon('ri.arrow-left-right-line', color='#ffffff'),
            lambda: root.goto_page('History')
        ),

    ]
    for button, icon, callback in buttons:
        if icon: button.setIcon(icon)
        if callback: button.clicked.connect(callback)

    # -- Callbacks
    root.close_msgs_frame(close=True)       # close the messages frame

    # -- ComboBox
    root.ui.comboBoxCategory.currentIndexChanged.connect(root.articles_by_category)
    root.ui.cbBoxUsersByGroup.currentIndexChanged.connect(root.users_by_groupe)
    root.ui.cbBoxCommandStatus.currentIndexChanged.connect(root.command_by_status)

    # --- LineEdits
    root.ui.lineEditSearch.textChanged.connect(root.search_article)
    root.ui.lineEditSearchUser.textChanged.connect(root.search_users)

    # --- TableWidgets
    root.ui.tableWidgetProduct.itemSelectionChanged.connect(lambda: root.enable_buttons(page='Magasin'))
    root.ui.tableWidgetProduct.itemDoubleClicked.connect(root.article_details)
    root.ui.tableWidgetUsers.itemSelectionChanged.connect(lambda: root.enable_buttons(page='Users'))
    root.ui.tableWidgetCommand.itemSelectionChanged.connect(lambda: root.enable_buttons(page='Commande'))

    # --- Menus
    def create_menu(menu_button, icon_name, actions, is_action_with_icon=False):
        """
        Helper function to create a menu for a given QPushButton.
        :param button: The QPushButton to which the menu will be attached.
        :param icon_name: The name of the icon to be set on the button.
        :param actions: A list of tuples where each tuple contains:
                        - The action name (str).
                        - The callback function (callable).
                        - Optional: The icon (if is_action_with_icon is True).
        :param is_action_with_icon: Boolean to determine if actions have associated icons.
        """
        menu_button.setIcon(qta.icon(icon_name, color='#ffffff'))
        menu = QtWidgets.QMenu(root)
        menu.setStyleSheet("""
        QMenu {
            background-color: rgb(33, 37, 43);
            border: 2px solid rgb(33, 37, 43);
            padding: 10px;
        }
        QMenu::item {
            color: rgb(255, 121, 198);
            padding: 8px 20px;
            background-color: transparent;
        }
        QMenu::item:selected {
            background-color: rgb(39, 44, 54);
        }
        """)

        for action in actions:
            if is_action_with_icon:
                action_name, callback, action_icon = action
                menu_label = menu.addAction(action_name)
                menu_label.setIcon(QtGui.QIcon(action_icon))
            else:
                action_name, callback = action
                menu_label = menu.addAction(action_name)
            menu_label.triggered.connect(callback)
        # setup the Menu
        menu_button.setMenu(menu)

    # -- Menu Product Actions
    product_actions = [
        # -- Alert Qte
        (
            'Quantité Alert', root.stock_alert,
            qta.icon('ph.alarm-light', color=WHITE_COLOR).pixmap(QtCore.QSize(25, 25))
        ),
        # -- Alert Price
        (
            'Price Alert', root.price_alert,
            qta.icon('ph.alarm-light', color=WHITE_COLOR).pixmap(QtCore.QSize(25, 25))
        ),
        # -- Sans Emplacement --
        (
            'Sans Emplacement', root.article_sans_emp,
            qta.icon('ph.list-numbers-light', color=WHITE_COLOR).pixmap(QtCore.QSize(25, 25))
        ),
        # -- Totals --
        (
            'Totals', root.total_article,
            qta.icon('ri.money-dollar-circle-fill', color=WHITE_COLOR).pixmap(QtCore.QSize(25, 25))
        ),
        # -- Empty Code --
        (
            'Code Viérge', root.empty_code,
            qta.icon('ri.search-line', color=WHITE_COLOR).pixmap(QtCore.QSize(25, 25))
        ),
    ]
    create_menu(root.ui.btnMenuProductActions, 'ri.arrow-down-s-line', product_actions, is_action_with_icon=True)


def widget_callbacks(root):
    """
    Setup all the callbacks for the widgets.
    """
    buttons = [
        # -- Save && Edit and Save Edit Buttons ---
        (root.ui.btnSaveNewCat, qta.icon('mdi.content-save', color=SAVE_COLOR), root.save_new_category),
        (root.ui.btnSaveNewArticle, qta.icon('mdi.content-save', color=SAVE_COLOR), root.save_new_article),
        (root.ui.btnEditArticle, qta.icon('mdi6.file-edit-outline', color="#F97F51"), root.toggle_edit_mode),
        (root.ui.btnSaveEditArticle, qta.icon('mdi6.content-save', color=SAVE_COLOR), root.update_article),
        (root.ui.btnSearchEmptyCode, qta.icon('ri.search-line', color=WHITE_COLOR), root.get_empty_code),

        # -- Entree Sortie Buttons ---
        (root.ui.btnSaveEntree, qta.icon('mdi6.content-save', color=SAVE_COLOR), root.save_entree),
        (root.ui.btnSaveSortie, qta.icon('mdi6.content-save', color=SAVE_COLOR), root.save_sortie),

        # --- Delete ---
        (root.ui.buttonConfirm, False, root.accept),        # close with True accept
        (root.ui.buttonCancel, False, root.close),          # close with False

        # -- Users --
        (root.ui.buttonLogin, qta.icon('ri.login-box-line', color="#ffffff"), root.handle_login),
        (root.ui.buttonSaveNewUser, qta.icon('mdi.content-save-outline', color=SAVE_COLOR), root.save_new_user),
        (root.ui.buttonSaveEditUser, qta.icon('mdi.content-save-outline', color=SAVE_COLOR), root.save_profile),
        (root.ui.buttonChangePassword, qta.icon('mdi.content-save-outline', color=SAVE_COLOR), root.save_new_password),

        # -- Commande
        (root.ui.btnSaveCommand, qta.icon('mdi.content-save-outline', color=SAVE_COLOR), root.save_command),
    ]
    for button, icon, callback in buttons:
        if icon: button.setIcon(icon)
        if callback: button.clicked.connect(callback)


class ArticleDialog(QtWidgets.QDialog):
    def __init__(self, user_id, db_handler):
        super().__init__()
        self.ui = Ui_Dialog()
        self.user_id = user_id
        self.db_handler = db_handler
        self.ui.setupUi(self)

        self.user = None
        self.edit_mode = False

        # Remove title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.contentTopBg.mouseMoveEvent = self.move_window  # to move window from the upBar

        # Hide Errors Label
        error_labels = [
            self.ui.labelNewError, self.ui.labelCategoryError, self.ui.labelEmptyCodeError,
            self.ui.labelEditError,
            self.ui.labelEntreeError, self.ui.labelSortieError,
            self.ui.labelAddUserErrors, self.ui.labelEditUserErrors, self.ui.labelLoginErrors, self.ui.labelChangePassErrors,
            self.ui.labelCommandError
        ]
        for label in error_labels:
            label.setText('')
            label.hide()

        # --- Setup Buttons ---
        widget_callbacks(self)
        self.setModal(True)     # Set Focus
        self.ui.closeAppBtn.clicked.connect(self.close)

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def move_window(self, e):
        """Move the window from upBar"""
        if not self.isMaximized():
            if e.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()

    def toggle_edit_mode(self):
        """
        Toggle the edit mode for the edit article.
        """
        self.edit_mode = not self.edit_mode  # Toggle state
        self.set_edit_mode(self.edit_mode)

    def populate_cbbox_category(self, comboBoxName):
        """
        Populate the combobox with categories from the database.
        """
        query = 'SELECT name FROM magasin_category ORDER BY cat_id'
        rows = self.db_handler.fetch_all(query)
        items = [row[0] for row in rows]
        # items.insert(0, 'Tous')
        utils.populate_comboBox(comboBoxName, items)

    def setup_label_id(self, label_id, item_id):
        """
        Set the label for the article ID.
        """
        label_id.setText(str(item_id))
        label_id.hide()

    def show_error(self, label_error, message='Une erreur est survenue'):
        """
        Show the error message on the label.
        """
        label_error.setText(message)
        label_error.show()

    def resize_dialog(self, current_page):
        """
        Resize the dialog based on the current page.
        Removes all other pages from the stackedWidget except the one to display.
        switch the stackedWidget to the current page.
        :param current_page: QWidget - the page to keep and show
        """
        # Remove all pages except the current one
        for i in reversed(range(self.ui.stackedWidget.count())):
            page = self.ui.stackedWidget.widget(i)
            if page != current_page:
                self.ui.stackedWidget.removeWidget(page)
        self.ui.stackedWidget.setCurrentWidget(current_page)        # Show the desired page
        # self.adjustSize()  # Automatically fit size
        self.resize(200, 100)

    # ------------------------------------------------------------------------------------
    # -- Article PAGE
    # ----------------
    def new_category(self):
        """
        Show the New Category Page
        """
        self.ui.titleLabel.setText("Nouvelle Catégorie")
        self.resize_dialog(current_page=self.ui.NewCategoryPage)

    def save_new_category(self):
        """
        Save the new category into the database.
        """
        cat_name = self.ui.lineEditCatName.text().upper()
        slug = cat_name.lower()
        logger.debug('INSERT category into database')
        query = 'INSERT INTO magasin_category(name, slug, created) VALUES(?, ?, ?)'
        result = self.db_handler.execute_query(query, [cat_name, slug, today])
        if result['success']:
            logger.info("✅ Catégorie ajoutée avec succès")
            self.ui.labelCategoryError.setText('')
            self.accept()
        else:
            logger.error(f"❌ Échec de l'ajout de la catégorie {result['message']}")
            if "UNIQUE constraint failed" in result["message"]:
                error_msg = "Catégory avec ce nom exist déja"
            else:
                error_msg = "Error lors de l'ajout. vérifier les donnée"
            self.show_error(self.ui.labelCategoryError, error_msg)

    def new_article(self):
        self.ui.titleLabel.setText("Nouvel Article")
        self.populate_cbbox_category(self.ui.cbBoxCatNew)
        self.resize_dialog(current_page=self.ui.NewArticlePage)

    def save_new_article(self):
        """
        Save the new article into the database.
        """
        category = self.ui.cbBoxCatNew.currentText()
        cat_id = self.db_handler.get_item_id('cat_id', 'magasin_category', 'name', category)
        code = self.ui.lineEditCodeNew.text().upper()
        slug = code.lower()

        desig = self.ui.lineEditDesigNew.text().title()
        ref = self.ui.lineEditRefNew.text().upper()
        um = self.ui.lineEditUMNew.text()
        emp = self.ui.lineEditEmpNew.text().upper() or '...'
        obs = self.ui.textEditObsNew.toPlainText()

        qte = self.ui.spinBoxQteNew.value()
        prix = self.ui.dSBoxPrixNew.value()
        valeur = qte * prix

        article_data = [today, cat_id, code, slug, desig, ref, um, emp, qte, prix, valeur, obs]
        result = self.db_handler.insert_new_article(article_data, code, today, qte, prix, self.user_id)
        if result['success']:
            logger.info(f"{result['message']} - Article ID: {result['lastrowid']}")
            self.accept()   # close the dialog
        else:
            logger.error(f"{result['message']}")
            self.show_error(self.ui.labelNewError, result['message'])

    def setup_empty_code(self):
        self.ui.titleLabel.setText("Code Viérge")
        self.populate_cbbox_category(self.ui.cbBoxCatEmptyCode)
        self.resize_dialog(current_page=self.ui.EmptyCodePage)

    def get_empty_code(self):
        """
        Get all empty codes in the selected category.
        """
        cat_name = self.ui.cbBoxCatEmptyCode.currentText()
        result = self.db_handler.get_all_missing_codes(cat_name)
        if result['success']:
            if len(result['missing_codes']) == 0:
                msg = "Aucun code viérge trouvé pour cette catégorie."
            else:
                msg = f"{', '.join(result['missing_codes'])}"
            self.ui.plainTextEditEmptyCodeResult.setPlainText(msg)
            self.resize_dialog(self.ui.EmptyCodePage)
        else:
            self.ui.labelEmptyCodeError.setText(f"Erreur: {result['message']}")

    # ----------------------------------------------------------------------------------
    def set_edit_mode(self, editable: bool):
        """
        Set the edit mode for the article update.
        """
        widgets = [
            self.ui.cbBoxCatEdit,
            self.ui.lineEditCodeEdit,
            self.ui.lineEditDesigEdit,
            self.ui.lineEditRefEdit,
            self.ui.lineEditUMEdit,
            self.ui.lineEditEmpEdit,
            self.ui.spinBoxQteEdit,
            self.ui.dSBoxPrixEdit,
            self.ui.dSBoxValeurEdit,
            self.ui.textEditObsEdit,
            self.ui.btnSaveEditArticle
        ]

        for widget in widgets:
            widget.setEnabled(editable)

    def article_details(self, art_id, edit_mode=False):
        """
        Show the article details.
        for editing we have a QPushButton
        :param art_id: int - the article ID
        :param edit_mode: bool - if True, set the edit mode
        """
        query = 'SELECT * FROM magasin_article WHERE art_id = ?'
        rows = self.db_handler.fetch_namedtuple(query, [art_id])
        if rows:
            article = rows[0]
            self.ui.titleLabel.setText('Fiche de Stock N° ' + str(art_id))
            self.setup_label_id(self.ui.labelArticleId, art_id)

            self.ui.lineEditCodeEdit.setText(f"{article.code}")
            self.ui.lineEditDesigEdit.setText(f"{article.designation}")
            self.ui.lineEditRefEdit.setText(f"{article.ref}")
            self.ui.lineEditUMEdit.setText(f"{article.umesure}")
            self.ui.lineEditEmpEdit.setText(f"{article.emp}")
            self.ui.spinBoxQteEdit.setValue(article.qte)
            self.ui.dSBoxPrixEdit.setValue(article.prix)
            self.ui.dSBoxValeurEdit.setValue(article.valeur)
            self.ui.textEditObsEdit.setPlainText(article.observation if article.observation else 'RAS')
            category_id = article.category_id

        category_name = self.db_handler.get_category_name(category_id)
        self.populate_cbbox_category(self.ui.cbBoxCatEdit)
        self.ui.cbBoxCatEdit.setCurrentText(category_name)
        self.set_edit_mode(editable=edit_mode)
        self.resize_dialog(current_page=self.ui.EditArticlePage)

    def update_article(self):
        """
        Update the article details in the database.
        """
        art_id = self.ui.labelArticleId.text()
        category = self.ui.cbBoxCatEdit.currentText()
        cat_id = self.db_handler.get_item_id('cat_id', 'magasin_category', 'name', category)
        code = self.ui.lineEditCodeEdit.text().upper()
        slug = code.lower()

        desig = self.ui.lineEditDesigEdit.text().title()
        ref = self.ui.lineEditRefEdit.text().upper()
        um = self.ui.lineEditUMEdit.text()
        emp = self.ui.lineEditEmpEdit.text().upper() or '...'
        obs = self.ui.textEditObsEdit.toPlainText()

        qte = self.ui.spinBoxQteEdit.value()
        prix = self.ui.dSBoxPrixEdit.value()
        valeur = qte * prix
        article_data = [cat_id, code, slug, desig, ref, um, emp, qte, prix, valeur, obs, art_id]

        logger.debug('-' * 30)
        logger.debug(f"Update Article with id: {art_id}")
        logger.debug(f"New Values: {article_data}")

        result = self.db_handler.update_article(article_data, art_id, code)
        if result['success']:
            logger.info("✅ Article mis à jour avec succès")
            self.set_edit_mode(False)
            self.edit_mode = not self.edit_mode  # Toggle state
            self.accept()  # close dialog if it's a QDialog
        else:
            logger.error(f"❌ Échec de la mise à jour de l'article {result['message']}")
            self.show_error(self.ui.labelEditError, f"{result['message']}")

    def confirm_dialog(self, msg):
        self.ui.titleLabel.setText("Confirmation")
        self.ui.confirmLabelMessage.setText(msg)
        self.resize_dialog(current_page=self.ui.ConfirmPage)

    # -----------------------------------------------------------------------------------
    def setup_entree_sortie(self, art_id, page):
        query = 'SELECT code, qte, prix FROM magasin_article WHERE art_id = ?'
        rows = self.db_handler.fetch_namedtuple(query, [art_id])
        if rows:
            article = rows[0]
            if page == 'Sortie':
                self.setup_label_id(self.ui.sortieArticleID, art_id)
                self.ui.titleLabel.setText("Nouvelle Sortie")
                self.ui.dateEditSortieDate.setDate(today)
                self.ui.lineEditSortieCode.setText(article.code)
                self.ui.spBoxSortiePrix.setValue(Decimal(article.prix))
                st_page = self.ui.SortiePage
            elif page == 'Entree':
                # Entree
                self.setup_label_id(self.ui.entreeArticleID, art_id)
                self.ui.titleLabel.setText("Nouvelle Entrée")
                self.ui.dateEditEntreeDate.setDate(today)
                self.ui.lineEditEntreeCode.setText(article.code)
                self.ui.spBoxEntreePrix.setValue(article.prix)
                st_page = self.ui.EntreePage

        self.resize_dialog(current_page=st_page)

    def save_entree(self):
        """
        Save the article entree
        """
        art_id = self.ui.entreeArticleID.text()
        query = 'SELECT * FROM magasin_article WHERE art_id = ?'
        article = self.db_handler.fetch_namedtuple(query, [art_id])[0]
        # --- Setup Entree Form --- #
        art_code = self.ui.lineEditEntreeCode.text().upper()
        ent_qte = self.ui.spBoxEntreeQte.value()
        ent_prix = self.ui.spBoxEntreePrix.value()
        ent_movdate = self.ui.dateEditEntreeDate.date().toPyDate()

        logger.debug('\nNouvel Entrée')
        logger.debug(f"Article: {article}")
        logger.debug(f'Entree: ({art_id})-({art_code})-({ent_movdate})-({ent_qte})-({ent_prix})')

        # --- Save the Form --- #
        result = self.db_handler.process_stock_entry(article, ent_qte, ent_prix, ent_movdate, self.user_id)
        # Check Qte and Prix for calculation
        if result['success']:
            logger.info("✅ Entrée ajoutée avec succès")
            self.accept()  # close dialog if it's a QDialog
        else:
            logger.error(f"❌ Échec de l'Entree: {result['message']}")
            self.show_error(self.ui.labelEntreeError, "Erreur lors de l'ajout de l'Entrée")
        logger.debug('\n')

    def save_sortie(self):
        art_id = self.ui.sortieArticleID.text()
        query = 'SELECT * FROM magasin_article WHERE art_id = ?'
        article = self.db_handler.fetch_namedtuple(query, [art_id])[0]

        # --- Setup sotie Form --- #
        sortie_movdate = self.ui.dateEditSortieDate.date().toPyDate()
        art_code = self.ui.lineEditSortieCode.text().upper()
        sortie_qte = self.ui.spBoxSortieQte.value()
        sortie_prix = self.ui.spBoxSortiePrix.value()

        logger.debug('\nNouvel Sortie')
        logger.debug(f"Article: {article}")
        logger.debug(f'Sortie: ({art_id})-({art_code})-({sortie_movdate})-({sortie_qte})-({sortie_prix})')

        # --- Save the Form --- #
        result = self.db_handler.process_stock_sortie(art_id, sortie_qte, sortie_movdate, self.user_id)
        # Check Qte and Prix for calculation
        if result['success']:
            logger.info("✅ Entrée ajoutée avec succès")
            self.accept()  # close dialog if it's a QDialog
        else:
            logger.error(f"❌ Échec de l'Entree: {result['message']}")
            self.show_message(self.ui.labelSortieError, "Erreur lors de l'ajout de l'Entrée")
        logger.debug('\n')

    # ------------------------------------------------------------------------------------
    # -- USERS PAGE
    # --------------
    def setup_login(self):
        logger.info('Getting User Credentials')
        self.ui.titleLabel.setText("Login")
        self.resize_dialog(current_page=self.ui.LoginPage)

    def handle_login(self):
        from dekhla import LoginManager
        username = self.ui.lineEditUsernameLogin.text().lower()
        password = self.ui.lineEditPasswordLogin.text()

        login_manager = LoginManager("./db.sqlite3")
        user = login_manager.authenticate(username, password)
        if user:
            logger.info('Login successful')
            self.user = user
            self.accept()
        else:
            logger.error('Login failed')
            self.show_error(self.ui.labelLoginErrors, "Nom d'utilisateur ou mot de passe incorrect.")

    def setup_new_user(self):
        self.ui.titleLabel.setText("Nouvel Utilisateur")
        self.resize_dialog(current_page=self.ui.NewUserPage)

    def save_new_user(self):
        username = self.ui.lineEditNewUsername.text().lower()
        email = self.ui.lineEditNewEmail.text()
        passwd = self.ui.lineEditNewPassword.text()
        r_passwd = self.ui.lineEditNewRePass.text()
        fname = self.ui.lineEditNewFName.text()
        lname = self.ui.lineEditNewLName.text()
        poste_travaille = self.ui.lineEditNewPTravaille.text()
        groupe = self.ui.cbBoxNewGroup.currentText().lower()
        logger.debug('-' * 30)
        logger.debug('Creating New User')
        result = self.db_handler.create_user(username, email, passwd, r_passwd, fname, lname, poste_travaille, groupe)
        if result['success']:
            logger.info("✅ Utilisateur créé avec succès")
            self.accept()  # close dialog if it's a QDialog
        else:
            logger.error(f"❌ Échec de la création de l'utilisateur {result['message']}")
            self.show_error(self.ui.labelAddUserErrors, f"{result['message']}")

    def setup_edit_user(self, user_id):
        query = """SELECT username, last_name, first_name, email, p.poste_travaille, p.groupe FROM auth_user
        JOIN accounts_profile p ON auth_user.id = p.user_id WHERE auth_user.id = ?
        """
        rows = self.db_handler.fetch_namedtuple(query, [user_id])
        if rows:
            user = rows[0]
            self.ui.titleLabel.setText(f"Fiche d'Utilisateur N°: {user_id}")
            self.setup_label_id(self.ui.labelEditUserID, user_id)

            self.ui.lineEditEditUsername.setText(user.username)
            self.ui.lineEditEditFName.setText(user.first_name)
            self.ui.lineEditEditLName.setText(user.last_name)
            self.ui.lineEditEditEmail.setText(user.email)
            self.ui.lineEditEditPTravaille.setText(user.poste_travaille)
            self.ui.cbBoxEditGroup.setCurrentText(user.groupe.title())

        self.resize_dialog(current_page=self.ui.EditUserPage)

    def save_profile(self):
        user_id = int(self.ui.labelEditUserID.text())
        username = self.ui.lineEditEditUsername.text().lower()
        email = self.ui.lineEditEditEmail.text()
        fname = self.ui.lineEditEditFName.text()
        lname = self.ui.lineEditEditLName.text()
        poste_travaille = self.ui.lineEditEditPTravaille.text().lower()
        groupe = self.ui.cbBoxEditGroup.currentText().lower()

        logger.debug('-' * 30)
        logger.debug(f'Update User with id: {user_id}')
        logger.debug(f"New Values: {username, fname, lname, email, poste_travaille, groupe}")

        result = self.db_handler.update_user(user_id, username, fname, lname, email, poste_travaille, groupe)
        if result['success']:
            logger.info("✅ Utilisateur mis à jour avec succès")
            self.accept()  # close dialog if it's a QDialog
        else:
            logger.error(f"❌ Échec de la mise à jour de l'utilisateur {result['message']}")
            self.show_error(self.ui.labelEditUserErrors, "Erreur lors de la mise à jour de l'utilisateur")

    def setup_change_password(self, user_id):
        self.ui.titleLabel.setText("Changer Mot de Passe")
        self.setup_label_id(self.ui.labelChangePasswordUserID, user_id)
        self.resize_dialog(current_page=self.ui.ChangePasswordPage)

    def save_new_password(self):
        user_id = self.ui.labelChangePasswordUserID.text()
        new_password = self.ui.lineEditChangePass.text()
        re_password = self.ui.lineEditReChangePass.text()
        logger.debug('-' * 30)
        logger.debug(f'save new password for user with id: {user_id}')
        logger.debug(f"Values: ({new_password})")
        result = self.db_handler.change_user_password(user_id, new_password, re_password)
        if result['success']:
            logger.info("✅ Mot de passe mise à jour avec succès")
            self.accept()  # close dialog if it's a QDialog
        else:
            logger.error(f"❌ Échec de la mise à jour de mot de passe {result['message']}")
            self.show_error(self.ui.labelChangePassErrors, f"{result['message']}")

    # ------------------------------------------------------------------------------------
    # -- COMMANDE PAGE
    # ----------------
    def setup_commande_page(self, art_id, art_code, user_id):
        self.ui.titleLabel.setText("Nouvelle Commande")
        self.setup_label_id(self.ui.commandArticleID, art_id)

        self.ui.dateEditCommandDate.setDate(today)
        self.ui.lineEditCommandCode.setText(art_code)
        self.ui.titleLabel.setText("Nouvelle Commande")
        self.resize_dialog(current_page=self.ui.NewCommandPage)

    def save_command(self):
        logger.debug('Saving new commande')
        art_id = self.ui.commandArticleID.text()
        command_date = self.ui.dateEditCommandDate.date().toPyDate()
        qte = self.ui.spBoxCommandQte.value()
        status = 0
        query = "INSERT INTO magasin_command(command_date, qte, art_id_id, user_id_id, status) VALUES(?, ?, ?, ?, ?)"
        params = [command_date, qte, art_id, self.user_id, 0]
        logger.debug('\nNouvel Commande')
        logger.debug(f'Commande: ({art_id})-({self.user_id})-({command_date})-({qte})-({status})')

        # --- Save the Form --- #
        result = self.db_handler.execute_query(query, params)

        if result['success']:
            logger.info("✅ Commande ajoutée avec succès")
            self.accept()  # close dialog if it's a QDialog
        else:
            logger.error(f"❌ Échec de l'Ajout de la Commande: {result['message']}")
            self.show_message(self.ui.labelCommandError, "Erreur lors de l'ajout de l'Entrée")
        logger.debug('\n')
