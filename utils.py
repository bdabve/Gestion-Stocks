from PyQt5 import QtWidgets

Error_COLOR = "#f77861"
Success_COLOR = "#44e37b"


def pagebuttons_stats(root):
    """
    Update page button states based on the current page.
    """
    current_page = root.ui.stackedWidget.currentIndex()
    root.ui.buttonMagasinPage.setChecked(current_page == 0)
    root.ui.buttonMovementPage.setChecked(current_page == 1)
    root.ui.buttonUsersPage.setChecked(current_page == 2)
    root.ui.buttonCommandePage.setChecked(current_page == 3)
    root.ui.buttonHistoryPage.setChecked(current_page == 4)


# Table Widget Functions
def populate_table_widget(table: QtWidgets.QTableWidget, rows: list, headers: list):
    """
    Populate a QTableWidget with rows and headers.

    :param table: The QTableWidget instance.
    :param rows: A list of rows where each row is a list or tuple of values.
    :param headers: A list of column headers.
    """
    table.clear()
    table.setSortingEnabled(False)
    table.setColumnCount(len(headers))
    table.setRowCount(len(rows))
    table.setHorizontalHeaderLabels(headers)

    for row_idx, row_data in enumerate(rows):
        for col_idx, value in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(value))
            table.setItem(row_idx, col_idx, item)

    table.horizontalHeader().setStretchLastSection(True)
    table.setSortingEnabled(True)
    table.resizeColumnsToContents()


def table_has_selection(table: QtWidgets.QTableWidget) -> bool:
    """
    Check if table has a selected rows
    :table: table widget name
    :return: True or False
    """
    if len(table.selectionModel().selectedRows()) > 0: return True
    else: return False


def get_column_value(table: QtWidgets.QTableWidget, row: int, column: int) -> str:
    """
    Get the value from a specific column of the selected row in a QTableWidget.

    :param table: The QTableWidget instance.
    :param column: The column index to retrieve the value from.
    :return: The value as a string.
    """
    # row = table.currentRow()
    return table.item(row, column).text()


def populate_comboBox(combobox: QtWidgets.QComboBox, items: list):
    """
    Populate a QComboBox with a list of items.

    :param combobox: The QComboBox instance.
    :param items: A list of strings to populate the combobox.
    """
    combobox.blockSignals(True)
    combobox.clear()
    combobox.addItems(items)
    combobox.blockSignals(False)
