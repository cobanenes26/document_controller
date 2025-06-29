# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

from modules import *

os.environ["QT_FONT_DPI"] = "96"  # Fix problem for High DPI and scale above 100%

widgets = None  # Global reference to UI widgets
warnings.filterwarnings("ignore", category=DeprecationWarning)


class MainWindow(QMainWindow):
    """
    Main application window class. Sets up the GUI and handles interaction logic.
    """

    APP_VERSION_MAJOR = 1
    APP_VERSION_MINOR = 0
    APP_VERSION_TEST = 0

    version = (
        f"V{APP_VERSION_MAJOR}.{APP_VERSION_MINOR}.{APP_VERSION_TEST}"
        + ("Unofficial" if APP_VERSION_TEST != 0 else "")
    )

    def __init__(self):
        """
        Initialize the main window, UI components, version label and connect events.
        """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        Settings.ENABLE_CUSTOM_TITLE_BAR = True  # Use custom title bar

        self.TITLE = "Document Controller"
        self.setWindowTitle(self.TITLE)

        widgets.version.setText(self.version)

        UIFunctions.uiDefinitions(self)

        self.home_page()
        self.fill_standarts()
        self.listener()
        self.show()

    def home_page(self):
        """
        Set the main stacked widget to the homepage and hide top/left UI sections.
        """
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.titleRightInfo.hide()
        widgets.leftMenuBg.hide()

    def fill_standarts(self):
        """
        Populate the standard selection combo box with YAML config files.
        """
        config_files = glob.glob("configs/*.yaml")
        widgets.comboBox.clear()
        for cfg_path in config_files:
            cfg_name = os.path.splitext(os.path.basename(cfg_path))[0]
            widgets.comboBox.addItem(cfg_name)

    def listener(self):
        """
        Connect UI buttons to their respective action handlers.
        """
        widgets.pushButton_urq0101.clicked.connect(
            lambda: widgets.stackedWidget.setCurrentWidget(widgets.page)
        )
        widgets.pushButton.clicked.connect(self.open_document)
        widgets.pushButton_2.clicked.connect(self.controller_func)
        widgets.pushButton_3.clicked.connect(self.home_page)

    def open_document(self):
        """
        Open a file dialog to select a PDF and show the path in the input field.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file_path:
            widgets.lineEdit.setText(file_path)
            self.document_path = Path(file_path)

    def controller_func(self):
        """
        Execute all validation rules on the selected PDF using the selected YAML config.
        """
        widgets.plainTextEdit.clear()
        widgets.pushButton.setDisabled(True)
        widgets.pushButton_2.setDisabled(True)
        widgets.comboBox.setDisabled(True)

        standard = widgets.comboBox.currentText().strip()
        pdf_path = getattr(self, "document_path", None)

        if not standard:
            widgets.plainTextEdit.appendPlainText("❌ No standard selected.")
            self._re_enable_controls()
            return

        if not pdf_path or not pdf_path.exists():
            widgets.plainTextEdit.appendPlainText("❌ No valid PDF selected.")
            self._re_enable_controls()
            return

        config = ConfigLoader.load_config(f"configs/{standard}.yaml")
        widgets.plainTextEdit.appendPlainText(
            f"Standard Applied: {config.get('standard_name', standard)}"
        )

        document_parser = DocumentParser()
        headings = document_parser.extract_headings(pdf_path)

        with pdf_path.open("rb") as f:
            import fitz
            doc = fitz.open(stream=f.read(), filetype="pdf")
            pages = [page.get_text() for page in doc]

        rules_engine = RulesEngine(config)
        missing_sections = rules_engine.check_required_sections(headings)

        if missing_sections:
            widgets.plainTextEdit.appendPlainText("Missing Sections:")
            for sec in missing_sections:
                widgets.plainTextEdit.appendPlainText(f" - {sec}")
        else:
            widgets.plainTextEdit.appendPlainText("All required sections are present.")

        if config.get("check_empty_sections", False):
            empty_checker = EmptySectionController(
                min_length=config.get("min_section_length", 30)
            )
            issues = empty_checker.check(pages, headings)
            if issues:
                widgets.plainTextEdit.appendPlainText(
                    "\\n⚠️ Empty or undersized sections:"
                )
                for issue in issues:
                    widgets.plainTextEdit.appendPlainText(f" - {issue['message']}")
            else:
                widgets.plainTextEdit.appendPlainText(
                    "\\n✅ No empty sections detected."
                )

        terminology_config = config.get("terminology_rules", {})
        if terminology_config:
            term_checker = TerminologyController(
                forbidden_words=terminology_config.get("forbidden_words", []),
                preferred_words=terminology_config.get("preferred_words", []),
            )
            term_issues = term_checker.check(pages)
            if term_issues:
                widgets.plainTextEdit.appendPlainText(
                    "\\n❌ Forbidden terminology detected:"
                )
                for issue in term_issues:
                    widgets.plainTextEdit.appendPlainText(f" - {issue['message']}")
            else:
                widgets.plainTextEdit.appendPlainText(
                    "\\n✅ No forbidden terminology found."
                )

        if config.get("check_heading_sequence", False):
            seq_checker = HeadingSequenceController()
            seq_issues = seq_checker.check(headings)
            if seq_issues:
                widgets.plainTextEdit.appendPlainText("\\n🔢 Heading sequence issues:")
                for issue in seq_issues:
                    widgets.plainTextEdit.appendPlainText(f" - {issue['message']}")
            else:
                widgets.plainTextEdit.appendPlainText(
                    "\\n✅ Heading sequence appears valid."
                )

        if config.get("check_reference_consistency", False):
            ref_checker = ReferenceConsistencyController()
            ref_issues = ref_checker.check(pages, headings)
            if ref_issues:
                widgets.plainTextEdit.appendPlainText(
                    "\\n📚 Reference consistency issues:"
                )
                for issue in ref_issues:
                    widgets.plainTextEdit.appendPlainText(f" - {issue['message']}")
            else:
                widgets.plainTextEdit.appendPlainText(
                    "\\n✅ All references used in text are defined in the reference list."
                )

        if config.get("check_image_dpi", False):
            img_checker = ImageQualityController(
                min_dpi=config.get("min_image_dpi", 150)
            )
            img_issues = img_checker.check(pdf_path)
            if img_issues:
                widgets.plainTextEdit.appendPlainText("\\n📸 Low DPI image warnings:")
                for issue in img_issues:
                    widgets.plainTextEdit.appendPlainText(
                        f" - Page {issue['page']} | DPI: {issue['dpi']} → {issue['message']}"
                    )
            else:
                widgets.plainTextEdit.appendPlainText(
                    "\\n✅ All images meet minimum DPI requirements."
                )

        if config.get("check_figure_table_references", False):
            ft_checker = FigureTableReferenceController()
            ft_issues = ft_checker.check(pages)
            if ft_issues:
                widgets.plainTextEdit.appendPlainText(
                    "\\n🧱 Figure/Table reference issues found:"
                )
                for issue in ft_issues:
                    widgets.plainTextEdit.appendPlainText(
                        f" - {issue['type']} {issue['ref']}: {issue['message']}"
                    )
            else:
                widgets.plainTextEdit.appendPlainText(
                    "\\n✅ All referenced figures and tables are defined."
                )

        if "concept_groups" in config:
            concept_checker = ConceptConsistencyController(config["concept_groups"])
            concept_issues = concept_checker.check(pages)
            if concept_issues:
                widgets.plainTextEdit.appendPlainText(
                    "\\n🧠 Concept consistency issues found:"
                )
                for issue in concept_issues:
                    widgets.plainTextEdit.appendPlainText(f" - {issue['message']}")
            else:
                widgets.plainTextEdit.appendPlainText(
                    "\\n✅ Concept usage is consistent."
                )

        self._re_enable_controls()

    def _re_enable_controls(self):
        """
        Re-enable UI controls after analysis is complete.
        """
        widgets.pushButton.setEnabled(True)
        widgets.pushButton_2.setEnabled(True)
        widgets.comboBox.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())