import os

import magic
import json
from typing import List

from cortex4py.query import *
from .abstract import AbstractController
from ..models import Analyzer, Job, AnalyzerDefinition
from .analyzers import AnalyzersController

class RespondersController(AnalyzersController):
    def __init__(self, api):
        AnalyzersController.__init__(self, 'responder', api)