import pandas as pd
from typing import Union, List, Optional

class MyDF(pd.DataFrame):
    idField = 'ID'
    def getRowByID(self, id):
        return self[self[self.idField] == id]
    def QuickSearch(self, searchField, searchKey, returnKey):
        return self[self[searchField] == searchKey].iloc[0][returnKey]
    def SearchContain(self, searchField, searchKey, returnKey):
        for i in range(0,len(self)):
            currentRow = self.iloc[i]
            if (searchKey in str(currentRow[searchField])):
                return currentRow[returnKey]
    def Compare(self, other: 'MyDF', 
                key_column: str = None,
                output_format: str = 'text',
                ignore_case: bool = False,
                ignore_whitespace: bool = False) -> Union[dict, str]:
        """
        Compare this MyDF with another MyDF, showing differences like Git, including row insertions/deletions.
        
        Parameters:
        - other: MyDF, the other DataFrame to compare with.
                - key_column: str, column to align rows (defaults to idField)
        - output_format: str, output format ('dict' or 'text')
        - ignore_case: bool, ignore case when comparing strings
        - ignore_whitespace: bool, trim whitespace when comparing strings
        
        Returns:
        - dict: {'changed': {(row_idx, column): (value1, value2)}, 'added': [row_idx], 'removed': [row_idx]}
        - str: Git-style text summary of differences
        """
        key = key_column if key_column else self.idField
        if key not in self.columns or key not in other.columns:
            raise ValueError(f"Key column '{key}' not found in one or both tables")
        
        if list(self.columns) != list(other.columns):
            raise ValueError("Table headers must be identical")
        
        # Create copies to handle case and whitespace
        df1 = self.copy()
        df2 = other.copy()
        
        if ignore_case or ignore_whitespace:
            for col in df1.columns:
                if df1[col].dtype == 'object':
                    if ignore_case:
                        df1[col] = df1[col].astype(str).str.lower()
                        df2[col] = df2[col].astype(str).str.lower()
                    if ignore_whitespace:
                        df1[col] = df1[col].astype(str).str.strip()
                        df2[col] = df2[col].astype(str).str.strip()
        
        # Align rows by key_column
        df1 = df1.set_index(key)
        df2 = df2.set_index(key)
        
        # Find common, added, and removed rows
        common_ids = df1.index.intersection(df2.index)
        added_rows = df2.index.difference(df1.index).tolist()
        removed_rows = df1.index.difference(df2.index).tolist()
        
        # Compare common rows
        differences = {'changed': {}, 'added': added_rows, 'removed': removed_rows}
        for idx in common_ids:
            for col in df1.columns:
                val1, val2 = df1.loc[idx, col], df2.loc[idx, col]
                if pd.isna(val1) and pd.isna(val2):
                    continue
                if val1 != val2:
                    differences['changed'][(idx, col)] = (val1, val2)
        
        # Format output
        if output_format == 'dict':
            return differences
        elif output_format == 'text':
            output = []
            # Report changed rows
            for (idx, col), (val1, val2) in differences['changed'].items():
                output.append(f"@@ Row {key}={idx} @@")
                output.append(f"- Column '{col}': {val1}")
                output.append(f"+ Column '{col}': {val2}")
            
            # Report added rows
            if added_rows:
                output.append("@@ Added rows @@")
                for idx in added_rows:
                    output.append(f"+ Row {key}={idx}: {dict(df2.loc[idx])}")
            # Report removed rows
            if removed_rows:
                output.append("@@ Removed rows @@")
                for idx in removed_rows:
                    output.append(f"- Row {key}={idx}: {dict(df1.loc[idx])}")
            return "\n".join(output) if output else "No differences found"
        else:
            raise ValueError("Invalid output_format. Choose 'dict' or 'text'.")
class ExTable(MyDF):
    def __init__(self, path, sheetName, skipRows = [], idField = "ID"):
        super().__init__(pd.read_excel(path, sheet_name = sheetName, skiprows=skipRows))
        self.idField = idField

class CSVTable(MyDF):
    def __init__(self, path, skipRows = [], idField = "---"):
        super().__init__(pd.read_csv(path, skiprows=skipRows))
        self.idField = idField