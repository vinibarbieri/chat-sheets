from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd

class SpreadsheetInterface(ABC):
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Carrega os dados da planilha."""
        pass

    @abstractmethod
    def save_data(self, data: List[Dict[str, str]]) -> None:
        """Salva os dados na planilha."""
        pass
