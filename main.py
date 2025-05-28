#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from datetime import date
from PyQt5 import QtWidgets, QtCore
import qtawesome as qta

import utils
import db_handler
from logger import logger
from uis.h_interface import Ui_MainWindow
from widgets import ArticleDialog
import widgets


class GestionStocks(QtWidgets.QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = user

        # Global Variable
        self.db_handler = db_handler.Database('./db.sqlite3')
        self.product_fields = widgets.product_fields
        self.product_headers = widgets.product_headers

        # TODO:  Add a context menu to actionbuttons
        # --- Callbacks
        widgets.interface_callbacks(self)
        # --- Starting Application
        self.initUi()

    def initUi(self):
        logger.info('Starting Application.')
        self.apply_role_permissions()
        self.display_date()
        self.goto_page('Magasin')

    # *******************************************************************
    #   => GLOBAL FUNCTIONS
    # ************************
    def apply_role_permissions(self):
        self.ui.labelUsername.setText(user.username.title())
        self.ui.labelUserGroupe.setText(user.groupe)

        buttons = [
            self.ui.buttonUsersPage,
            self.ui.newEntryBtn, self.ui.newSortieBtn, self.ui.editArticleBtn, self.ui.delArticleBtn,
            self.ui.newCommandBtn,
            self.ui.editUserBtn, self.ui.delUserBtn
        ]
        if self.user.groupe != 'admin':
            logger.info('User is not admin, disabling buttons.')
            for btn in buttons:
                btn.hide()

    def get_item_id(self, tableWidget):
        """
        This return the current selected row and column 0, item ID from tableWidget
        :tableWidget: the table widget to get item
        """
        if utils.table_has_selection(tableWidget):
            row = tableWidget.currentRow()
            item_id = utils.get_column_value(tableWidget, row, 0)
            return item_id

    def show_error_message(self, message, success=False):
        """
        Show an animated error or success message inside the frame.
        Auto-hide if success.

        Args:
            message (str): The message to display.
            success (bool): If True, color is green and auto-close after timeout.
        """
        label = self.ui.labelMsgs
        label.setText(message)
        close_button = self.ui.buttonCloseMsgsFrame

        btn_ssheet = 'background: transparent; border-radius: 0; border-top-right-radius: 5px; border-bottom-right-radius: 5px'
        label_ssheet = 'background: transparent; padding: 5px 7px; border-top-left-radius: 5px; border-bottom-left-radius: 5px; '
        frame_ssheet = 'border-radius: 5px 7px; '
        if success:
            # Green for success
            frame_ssheet += 'background-color: rgba(60, 184, 127, 47);'
            label_ssheet += 'color: #44e37b'

            self.ui.frameMsgs.setStyleSheet(frame_ssheet)
            label.setStyleSheet(label_ssheet)
            close_button.setIcon(qta.icon('ph.x-light', color=utils.Success_COLOR))
            close_button.setStyleSheet(btn_ssheet)

            # Start timer to auto-close after 3 seconds
            self.auto_close_timer = QtCore.QTimer()
            self.auto_close_timer.setSingleShot(True)
            self.auto_close_timer.timeout.connect(lambda: self.close_msgs_frame(close=True))
            self.auto_close_timer.start(3000)  # 3000 milliseconds = 3 seconds
        else:
            frame_ssheet += 'background: #3b3230;'
            label_ssheet += 'color: #f77861'

            # StyleSheets
            self.ui.frameMsgs.setStyleSheet(frame_ssheet)
            label.setStyleSheet(label_ssheet)
            close_button.setIcon(qta.icon('ph.x-light', color=utils.Error_COLOR))
            close_button.setStyleSheet(btn_ssheet)
        # Open the frame
        self.close_msgs_frame(close=False)

    def close_msgs_frame(self, close=True):
        """
        Animate the height of the QTextBrowser.
        :close: bool True to close; False to open
        """
        msgs_frame = self.ui.frameMsgs
        width = msgs_frame.maximumWidth()
        new_width = 0 if close else 400
        # Create the animation object
        self.close_animation = QtCore.QPropertyAnimation(msgs_frame, b"maximumWidth")
        self.close_animation.setDuration(250)  # Duration in milliseconds
        self.close_animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.close_animation.setStartValue(width)
        self.close_animation.setEndValue(new_width)

        # Start the animation
        self.close_animation.start()

    def display_records(self, page, rows, label_count, msg=None):
        """
        Display records in the appropriate table widget based on the page.
        switch the stackedWidget to the appropriate page
        :page: Products, Movement, Users
        :rows: the result from the database
        :label_count: the label that display the count
        :msg: message to display in the count label
        """
        if page == 'Products':
            headers = self.product_headers
            tableWidget = self.ui.tableWidgetProduct
            st_page = self.ui.MagasinPage

        elif page == 'Movements':
            headers = ['Date', 'User', 'Operation', 'Code', 'Designaton', 'Qte', 'Prix']
            tableWidget = self.ui.tableWidgetMovement
            st_page = self.ui.MovementPage

        elif page == 'Users':
            headers = ['ID', 'Last Login', 'Username', 'Email', 'First Name', 'Last Name',
                       'Poste Travaille', 'Groupe', 'Date Joined',]
            tableWidget = self.ui.tableWidgetUsers
            st_page = self.ui.UsersPage

        elif page == 'Commande':
            headers = ['ID', 'Date', 'User', 'Code', 'Designation', 'Qte', 'Status']
            tableWidget = self.ui.tableWidgetCommand
            st_page = self.ui.CommandePage

        if msg:
            label_count.setText(f"{msg} ({len(rows)})")
        else:
            label_count.setText(f"Total {page}: {len(rows)}.")

        utils.populate_table_widget(tableWidget, rows, headers)
        self.ui.stackedWidget.setCurrentWidget(st_page)

    # -- Toggle Left Menu and Left Box Settings (not implemented yet) --
    def toggle_menu(self, action='open'):
        """
        This will animate the Client/Product badge up/down
        :frame: the frame to animate (product_badge | client_badge)
        :button: the button to change his icon
        """
        frame = self.ui.leftMenuBg
        width = frame.width()
        new_width = 220 if width == 60 else 60

        self.anim_left_frame = QtCore.QPropertyAnimation(frame, b'minimumWidth')  # wont work without self
        self.anim_left_frame.setDuration(250)
        self.anim_left_frame.setStartValue(width)
        self.anim_left_frame.setEndValue(new_width)
        self.anim_left_frame.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.anim_left_frame.start()

    def toggle_left_box(self, close=False):
        """
        This will animate the Client/Product badge up/down
        :frame: the frame to animate (product_badge | client_badge)
        :button: the button to change his icon
        """
        frame = self.ui.extraLeftBox
        width = frame.width()
        # if close:
            # new_width = 0
        # else:
            # new_width = 31
        new_width = 0 if width == 313 else 313

        self.anim_left_frame = QtCore.QPropertyAnimation(frame, b'minimumWidth')  # wont work without self
        self.anim_left_frame.setDuration(250)
        self.anim_left_frame.setStartValue(width)
        self.anim_left_frame.setEndValue(new_width)
        self.anim_left_frame.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.anim_left_frame.start()

    # -- Switch between Pages -- Enable or disable Buttons --
    def goto_page(self, page: str):
        """
        Navigate to the specified page and update UI elements accordingly.
        :param page: Page to navigate to (Products | Customers | Orders).
        """
        if page == 'Magasin':
            # Display all products
            self.display_all_products()
            self.display_categories()
            self.enable_buttons(page='Magasin')
            self.ui.stackedWidget.setCurrentWidget(self.ui.MagasinPage)

        elif page == 'Movements':
            # this is the init movement display
            self.display_all_movements()
            self.ui.stackedWidget.setCurrentWidget(self.ui.MovementPage)

        elif page == 'Users':
            self.display_all_users()
            self.enable_buttons(page='Users')
            self.ui.stackedWidget.setCurrentWidget(self.ui.UsersPage)

        elif page == 'Commande':
            self.display_all_commande()
            self.enable_buttons(page='Commande')
            self.ui.stackedWidget.setCurrentWidget(self.ui.CommandePage)

        elif page == 'History':
            self.ui.stackedWidget.setCurrentWidget(self.ui.HistoryPage)

        utils.pagebuttons_stats(self)

    def enable_buttons(self, page='Magasin'):
        """
        Enable or disable buttons(edit, remove) based on the current page and selection.
        This function work also with tableWidget.currentIndexChanged
        """
        if page == 'Magasin':
            tableWidget = self.ui.tableWidgetProduct
            buttons = (
                self.ui.newEntryBtn,
                self.ui.newSortieBtn,
                self.ui.editArticleBtn,
                self.ui.delArticleBtn,
                self.ui.newCommandBtn,
            )
            # Movement Button
            if utils.table_has_selection(self.ui.tableWidgetProduct):
                row = self.ui.tableWidgetProduct.currentRow()
                art_id = utils.get_column_value(self.ui.tableWidgetProduct, row, 0)
                article_has_movement = self.db_handler.article_has_movement(art_id)
                # Disconnect previous connections
                if article_has_movement:
                    self.ui.movArticleBtn.setEnabled(True)
                    try:
                        self.ui.movArticleBtn.clicked.disconnect()
                    except TypeError:
                        pass
                    self.ui.movArticleBtn.clicked.connect(lambda: self.article_movements(art_id))
                else:
                    self.ui.movArticleBtn.setEnabled(False)
            else:
                self.ui.movArticleBtn.setEnabled(False)

        elif page == 'Users':
            tableWidget = self.ui.tableWidgetUsers
            buttons = (
                self.ui.editUserBtn,
                self.ui.changePasswordBtn,
                self.ui.delUserBtn
            )
        elif page == 'Commande':
            tableWidget = self.ui.tableWidgetCommand
            cmd_id = self.get_item_id(tableWidget)
            cmd_active = self.db_handler.commande_status(cmd_id)
            self.ui.activeCommandBtn.setEnabled(cmd_active)
            buttons = (
                self.ui.editCommandBtn,
                self.ui.delCommandBtn
            )

        # Enable/disable all buttons
        for btn in buttons:
            btn.setEnabled(utils.table_has_selection(tableWidget))

    def display_date(self):
        """
        Display Hijri and Milady Date in Labels
        """
        # display date
        from ummalqura.hijri_date import HijriDate
        tday = date.today()
        hijri = HijriDate(tday.year, tday.month, tday.day, gr=True)
        hijri = '{}: {} {} {}'.format(hijri.day_name, hijri.day, hijri.month_name, hijri.year)
        tday = date.today().strftime('%A %d %b %Y')

        self.ui.labelDate.setText(str(tday))
        self.ui.labelHijri.setText(str(hijri))

    # -- Menu Functions --
    def stock_alert(self):
        """
        Display all stocks that have quantity = 0
        """
        query = f'SELECT {", ".join(self.product_fields)} FROM magasin_article WHERE qte = ?'
        rows = self.db_handler.fetch_all(query, [0])
        msg = 'Quantité égale a 0'
        self.display_records('Products', rows, self.ui.labelProductsCount, msg)

    def price_alert(self):
        query = f'SELECT {", ".join(self.product_fields)} FROM magasin_article WHERE prix = ?'
        rows = self.db_handler.fetch_all(query, [0])
        msg = 'Article Sans Prix'
        self.display_records('Products', rows, self.ui.labelProductsCount, msg)

    def article_sans_emp(self):
        query = f'SELECT {", ".join(self.product_fields)} FROM magasin_article WHERE emp = ?'
        rows = self.db_handler.fetch_all(query, ['...'])
        msg = 'Article Sans Emplacement'
        self.display_records('Products', rows, self.ui.labelProductsCount, msg)

    def total_article(self):
        query = 'SELECT COUNT(art_id), SUM(valeur), SUM(qte) FROM magasin_article'
        rows = self.db_handler.fetch_all(query)
        for row in rows:
            total_article, valeur, total_qte = row
            # TODO:  Display this in a new window
            logger.debug(f"t_article({total_article}); t_valeur({valeur}); t_qte({total_qte})")

    # *****************************************************************
    #   => Products Page
    # *******************
    def display_categories(self):
        """
        Display categories in the comboBoxCategory
        """
        query = 'SELECT name FROM magasin_category ORDER BY cat_id'
        rows = self.db_handler.fetch_all(query)
        items = [row[0] for row in rows]
        items.insert(0, 'Tous')
        utils.populate_comboBox(self.ui.comboBoxCategory, items)

    def display_all_products(self):
        """
        Dump all records from magasin_article SQL Table
        """
        logger.info('Dump All Records from magasin_article Table')
        query = f"SELECT {', '.join(self.product_fields)} FROM magasin_article ORDER BY code"
        rows = self.db_handler.fetch_all(query)
        self.display_records('Products', rows, self.ui.labelProductsCount)

    def articles_by_category(self):
        """
        Display Articles By Category
        """
        category = self.ui.comboBoxCategory.currentText()
        category_id = self.db_handler.get_item_id('cat_id', 'magasin_category', 'name', category)
        logger.debug(f"Get Articles By Category: Category( {category_id} - {category_id})")
        if category == 'Tous':
            self.display_all_products()
        else:
            query = f"""SELECT {', '.join(self.product_fields)} FROM magasin_article
                        WHERE category_id = ? ORDER BY code"""
            rows = self.db_handler.fetch_all(query, [category_id])
            self.display_records('Products', rows, self.ui.labelProductsCount)

    def search_article(self):
        """
        Search Articles
        """
        search_word = self.ui.lineEditSearch.text()
        if not search_word:
            return  # or show a message to the user that the search input is empty
        else:
            msg = f"Recherche Par: {search_word}"     # Set a title indicating the search term used
            search_word = f"%{search_word}%"

        query = f"""
            SELECT {', '.join(self.product_fields)}
            FROM magasin_article
            WHERE code LIKE ?
            OR designation LIKE ?
            OR ref LIKE ?
        """
        params = [search_word, search_word, search_word]
        rows = self.db_handler.fetch_all(query, params)
        msg += f" ( {len(rows)} )"
        self.display_records('Products', rows, self.ui.labelProductsCount)

    def article_movements(self, art_id):
        """
        Display all movements for the selected article
        """
        logger.debug(f'Get Movements for article with ID ({art_id}).')

        rows = self.db_handler.article_movements(art_id)
        self.display_records('Movements', rows, self.ui.labelMovementsCount)
        utils.pagebuttons_stats(self)

    def empty_code(self):
        logger.debug('Search Empty Code')
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.setup_empty_code()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # self.show_error_message('Catégorie ajoutée avec succès', success=True)
            self.goto_page('Magasin')

    # *************************************************************************
    #   => Article Operation(New, details, edit, entree, sortie) Page
    # *****************************************************************
    def new_category(self):
        """
        Open the dialog for new category
        """
        logger.debug('Adding new catégory.')
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.new_category()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Catégorie ajoutée avec succès', success=True)
            self.goto_page('Magasin')

    def new_article(self):
        """
        Open the dialog for new article
        """
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.new_article()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Article ajouté avec succès', success=True)
            self.goto_page('Magasin')

    def article_details(self):
        """
        Open the dialog for article details and update
        """
        art_id = self.get_item_id(self.ui.tableWidgetProduct)
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.article_details(art_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Article modifié avec succès', success=True)
            self.goto_page('Magasin')

    def edit_article(self):
        """
        This will open the article detail with edit mode enabled
        """
        art_id = self.get_item_id(self.ui.tableWidgetProduct)
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.article_details(art_id, edit_mode=True)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Article modifié avec succès', success=True)
            self.goto_page('Magasin')

    def article_new_entry(self):
        """
        Open the dialog for Nouvelle Entrée
        """
        art_id = self.get_item_id(self.ui.tableWidgetProduct)
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.setup_entree_sortie(art_id, 'Entree')
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Entrée Ajouté avec succés', success=True)
            self.goto_page('Magasin')

    def article_new_sortie(self):
        """
        Open the dialog for Nouvelle Sortie
        """
        art_id = self.get_item_id(self.ui.tableWidgetProduct)
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.setup_entree_sortie(art_id, 'Sortie')
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Sortie Ajouté avec succés', success=True)
            self.goto_page('Magasin')

    def delete_article(self):
        """
        Delete Article
        """
        art_id = self.get_item_id(self.ui.tableWidgetProduct)
        logger.debug(f'Confirm delete article ID: {art_id}')

        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        msg = f"Voulez-vous vraiment supprimer l'article avec ID: {art_id} ?\n Cette action ne peut pas être annulée."
        dialog.confirm_dialog(msg)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            query = "DELETE FROM magasin_article WHERE art_id = ?"
            result = self.db_handler.execute_query(query, [art_id])
            if result['success']:
                logger.info(f'Article with ID: {art_id} deleted successfully.')
                self.show_error_message('Article supprimé avec succès', success=True)
                self.goto_page('Magasin')
            else:
                self.show_error_message("Erreur lors de la suppression de l'article", success=False)
                logger.debug(f"Error deleting article {result['message']}")
        else:
            logger.debug('Cancel Deleting')

    # *************************************************************************
    # --- USERS PAGE ---
    # ********************
    def display_all_users(self):
        """
        Display all users from the database
        """
        logger.info('Display all Users from database.')
        query = f"""
        SELECT {', '.join(widgets.user_fields)} FROM auth_user
        LEFT JOIN accounts_profile AS p ON auth_user.id = p.user_id ORDER BY date_joined DESC
        """
        rows = self.db_handler.fetch_all(query)
        self.display_records('Users', rows, self.ui.labelUsersCount)

    def search_users(self):
        """
        Search for users matching the keyword in username, email, first_name, or last_name.

        Parameters:
            keyword (str): the search keyword.
        """
        keyword = self.ui.lineEditSearchUser.text()
        # logger.info(f'Search users with keyword: {keyword}')
        query = f"""
        SELECT {', '.join(widgets.user_fields)}
        FROM auth_user
        LEFT JOIN accounts_profile AS p ON auth_user.id = p.user_id
        WHERE username LIKE ?
            OR email LIKE ?
            OR first_name LIKE ?
            OR last_name LIKE ?
            OR p.poste_travaille LIKE ?
        ORDER BY date_joined DESC
        """
        like_keyword = f"%{keyword}%"
        rows = self.db_handler.fetch_all(query, (like_keyword,) * 5)
        self.display_records('Users', rows, self.ui.labelUsersCount)

    def users_by_groupe(self):
        """
        Display Users By Groupe
        """
        groupe = self.ui.cbBoxUsersByGroup.currentText().lower()
        logger.debug(f"Getting user by groupe: {groupe}")
        if groupe == 'tous':
            self.display_all_users()
        else:
            query = f"""
            SELECT {', '.join(widgets.user_fields)} FROM auth_user
            INNER JOIN accounts_profile AS p ON auth_user.id = p.user_id
            WHERE groupe = ? ORDER BY date_joined DESC
            """
            rows = self.db_handler.fetch_all(query, [groupe])
            self.display_records('Users', rows, self.ui.labelUsersCount)

    def new_user(self):
        """
        Open the dialog for new user
        """
        logger.debug('Adding new User.')
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.setup_new_user()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # self.show_error_message('Utilisateur ajouté avec succès', success=True)
            self.goto_page('Users')

    def edit_user(self):
        """
        Open the dialog for user details and update
        """
        user_id = self.get_item_id(self.ui.tableWidgetUsers)
        logger.debug(f"Edit User ID: {user_id}")
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.setup_edit_user(user_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Utilisateur modifié avec succès', success=True)
            self.goto_page('Users')

    def change_password(self):
        """
        Open the dialog for change password
        """
        user_id = self.get_item_id(self.ui.tableWidgetUsers)
        logger.debug(f"Change Password for User ID: {user_id}")
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.setup_change_password(user_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Mot de passe mis à jour avec succés.', success=True)
            self.goto_page('Users')

    def delete_user(self):
        """
        Delete User from database
        """
        user_id = self.get_item_id(self.ui.tableWidgetUsers)
        logger.debug(f"Confirm Delete User ID: {user_id}")

        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        msg = f"Voulez-vous vraiment supprimer l'utilisateur avec ID: {user_id} ?\n Cette action ne peut pas être annulée."
        dialog.confirm_dialog(msg)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            query = "DELETE FROM auth_user WHERE id = ?"
            result = self.db_handler.execute_query(query, [user_id])
            if result['success']:
                logger.info(f'User with ID: {user_id} deleted successfully.')
                self.show_error_message('Utilisateur supprimé avec succès', success=True)
                self.goto_page('Users')
            else:
                self.show_error_message("Erreur lors de la suppression de l'utilisateur", success=False)
                logger.error(f"Error deleting user {result['message']}")
        else:
            logger.info('Cancel Deleting User.')

    # *************************************************************************
    # --- MOVEMENT PAGE ---
    # **********************
    def display_all_movements(self):
        """
        Dump all records from magasin_movement SQL Table
        """
        logger.info('Dump all Movements from magasin_movement SQL Table.')
        query = """SELECT DATE(mov.movement_date) AS mov_date, user.username, mov.movement, art.code,
                    art.designation, mov.qte, mov.prix
                    FROM magasin_movement AS mov
                    INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
                    INNER JOIN auth_user AS user ON user.id = mov.user_id_id
                    ORDER BY mov_date DESC"""
        rows = self.db_handler.fetch_all(query)
        self.display_records('Movements', rows, self.ui.labelMovementsCount)

    def search_movements(self):
        code = self.ui.lineEditSearchMov.text().strip()
        operation = self.ui.cbBoxMovementOperation.currentText()
        if operation == 'Tous': operation = None

        date_selected = self.ui.dateEditMov.date().toPyDate() if self.ui.checkBoxSearchMovDate.isChecked() else None

        filters = []
        params = []

        if code:
            code_query = "SELECT art_id FROM magasin_article WHERE code LIKE ?"
            code_result = self.db_handler.fetch_all(code_query, [f"%{code}%"])
            art_ids = [row[0] for row in code_result]

            if art_ids:
                placeholders = ','.join(['?'] * len(art_ids))
                filters.append(f"art_id_id IN ({placeholders})")
                params.extend(art_ids)
            else:
                # No matching articles found, show a message or handle accordingly
                return

        if operation:
            filters.append("movement = ?")
            params.append(operation)

        if date_selected:
            filters.append("DATE(movement_date) LIKE ?")
            params.append(date_selected.strftime("%Y-%m-%d"))  # SQLite expects 'YYYY-MM-DD'

        # Compose final SQL
        base_query = '''
        SELECT DATE(mov.movement_date) AS mov_date, user.username, mov.movement, art.code, art.designation, mov.qte, mov.prix
        FROM magasin_movement AS mov
        INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
        INNER JOIN auth_user AS user ON user.id = mov.user_id_id
        '''
        if filters:
            base_query += " WHERE " + " AND ".join(filters)
        base_query += " ORDER BY movement_date DESC"

        results = self.db_handler.fetch_all(base_query, params)
        self.display_records('Movements', results, self.ui.labelMovementsCount)

    # *************************************************************************
    # --- COMMANDE PAGE ---
    # **********************
    def display_all_commande(self):
        """
        Dump all records from magasin_command SQL Table
        """
        logger.debug('Display all Commandes from database.')
        query = """SELECT cmd.command_id, DATE(cmd.command_date) AS cmd_date, user.username,
                    art.code, art.designation, cmd.qte, cmd.status
                    FROM magasin_command AS cmd
                    LEFT JOIN magasin_article AS art ON cmd.art_id_id = art.art_id
                    LEFT JOIN auth_user AS user ON user.id = cmd.user_id_id
                    ORDER BY cmd.command_date DESC"""
        rows = self.db_handler.fetch_all(query)
        self.display_records('Commande', rows, self.ui.labelCommandCount)

    def command_by_status(self):
        """
        Display Commandes By Status
        1 => Active
        0 => Inactive
        """
        status = self.ui.cbBoxCommandStatus.currentText().lower()
        if status == 'tous':
            self.display_all_commande()
        else:
            sts = 1 if status == 'active' else 0
            query = """SELECT cmd.command_id, DATE(cmd.command_date) AS cmd_date, user.username,
                        art.code, art.designation, cmd.qte, cmd.status
                        FROM magasin_command AS cmd
                        INNER JOIN magasin_article AS art ON cmd.art_id_id = art.art_id
                        INNER JOIN auth_user AS user ON user.id = cmd.user_id_id
                        WHERE cmd.status = ?
                        ORDER BY cmd.command_date DESC"""
            rows = self.db_handler.fetch_all(query, [sts])
            self.display_records('Commande', rows, self.ui.labelCommandCount)

    def new_commande(self):
        """
        Open the dialog for new commande
        """
        art_id = self.get_item_id(self.ui.tableWidgetProduct)
        art_code = utils.get_column_value(self.ui.tableWidgetProduct, self.ui.tableWidgetProduct.currentRow(), 1)
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.setup_commande_page(art_id, art_code, self.user.id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            logger.debug('Adding new commande.')
            self.show_error_message('Commande Ajouté avec succés', success=True)
            self.goto_page('Commande')

    def commande_details(self):
        """
        Open the dialog for article details and update
        """
        art_id = self.get_item_id(self.ui.tableWidgetCommand)
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.commande_details(art_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Commande modifié avec succès', success=True)
            self.goto_page('Commande')

    def edit_commande(self):
        """
        This will open the article detail with edit mode enabled
        """
        cmd_id = self.get_item_id(self.ui.tableWidgetCommand)
        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        dialog.commande_details(cmd_id, edit_mode=True)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.show_error_message('Commande modifié avec succès', success=True)
            self.goto_page('Commande')

    def delete_commande(self):
        """
        Delete Commande from database
        """
        cmd_id = self.get_item_id(self.ui.tableWidgetCommand)
        logger.debug(f'Confirm delete Commande ID: {cmd_id}')

        dialog = ArticleDialog(user_id=self.user.id, db_handler=self.db_handler)
        msg = f"Voulez-vous vraiment supprimer la commande avec ID: {cmd_id} ?\n Cette action ne peut pas être annulée."
        dialog.confirm_dialog(msg)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            query = "DELETE FROM magasin_command WHERE command_id = ?"
            result = self.db_handler.execute_query(query, [cmd_id])
            if result['success']:
                logger.info(f'Command with ID: {cmd_id} deleted successfully.')
                self.show_error_message('Commande supprimé avec succès', success=True)
                self.goto_page('Commande')
            else:
                self.show_error_message("Erreur lors de la suppression de la Commande", success=False)
                logger.debug(f"Error deleting Commande {result['message']}")
        else:
            logger.debug('Cancel Deleting')

    def activate_command(self):
        """
        Activate Commande
        set the status to 1 (active) in the database
        """
        cmd_id = self.get_item_id(self.ui.tableWidgetCommand)
        query = "UPDATE magasin_command SET status = 1 WHERE command_id = ?"
        result = self.db_handler.execute_query(query, [cmd_id])
        if result['success']:
            logger.info(f'Command with ID: {cmd_id} activated successfully.')
            self.show_error_message('Commande activée avec succès', success=True)
            self.goto_page('Commande')
        else:
            self.show_error_message("Erreur lors de l'activation de la Commande", success=False)
            logger.debug(f"Error activating Commande {result['message']}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # Login and startAPP
    # dialog = widgets.ArticleDialog(db_handler=None)
    # dialog.setup_login()
    # if dialog.exec_() == QtWidgets.QDialog.Accepted:
        # user = dialog.user
        # w = GestionStocks(user)
        # w.showMaximized()
        # sys.exit(app.exec_())
    from dekhla import LoginManager
    login_manager = LoginManager("./db.sqlite3")
    username = 'admin'
    password = 'admin_magasin'
    user = login_manager.authenticate(username, password)
    if user:
        w = GestionStocks(user)
        w.showMaximized()
        sys.exit(app.exec_())
    else:
        print("Identifiants incorrects.")
