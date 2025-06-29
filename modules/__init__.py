# /////////////////////////////////////////
# BY: Enes COBAN
# /////////////////////////////////////////

import argparse
import os
import sys
import glob
import warnings
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path

from modules.config_loader import ConfigLoader
from modules.document_parser import DocumentParser
from modules.rules_engine import RulesEngine
from modules.report_generator import ReportGenerator
from modules.controllers.empty_section_controller import EmptySectionController
from modules.controllers.terminology_controller import TerminologyController
from modules.controllers.heading_sequence_controller import HeadingSequenceController
from modules.controllers.reference_consistency_controller import ReferenceConsistencyController
from modules.controllers.image_quality_controller import ImageQualityController
from modules.controllers.figure_table_controller import FigureTableReferenceController
from modules.controllers.concept_consistency_controller import ConceptConsistencyController

from ui.ui_main import Ui_MainWindow
from ui.ui_functions import UIFunctions
from ui.app_settings import Settings