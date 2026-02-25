"""
Data Export Filter Module
Allows users to filter data before exporting to download only relevant information.
"""

class DataExportFilter:
    def __init__(self, data):
        """
        Initialize the filter with data to be exported.
        
        Args:
            data: List of dictionaries containing the data to filter
        """
        self.data = data
        self.filtered_data = []
    
    def filter_by_date_range(self, start_date, end_date, date_field='created_at'):
        """
        Filter data by date range.
        
        Args:
            start_date: Start date for filtering (string format: YYYY-MM-DD)
            end_date: End date for filtering (string format: YYYY-MM-DD)
            date_field: Field name containing the date
        
        Returns:
            List of filtered records
        """
        filtered = []
        for record in self.data:
            if date_field in record:
                record_date = record[date_field]
                # BUG: Using string comparison instead of proper date comparison
                if start_date <= record_date <= end_date:
                    filtered.append(record)
        
        self.filtered_data = filtered
        return filtered
    
    def filter_by_category(self, categories):
        """
        Filter data by category.
        
        Args:
            categories: List of categories to include
        
        Returns:
            List of filtered records
        """
        filtered = []
        for record in self.data:
            if 'category' in record and record['category'] in categories:
                filtered.append(record)
        
        self.filtered_data = filtered
        return filtered
    
    def filter_by_value_range(self, field, min_value, max_value):
        """
        Filter data by numeric value range.
        
        Args:
            field: Field name to filter on
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)
        
        Returns:
            List of filtered records
        """
        filtered = []
        for record in self.data:
            if field in record:
                value = record[field]
                if min_value <= value <= max_value:
                    filtered.append(record)
        
        self.filtered_data = filtered
        return filtered
    
    def export_to_csv(self, filename):
        """
        Export filtered data to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        import csv
        
        if not self.filtered_data:
            print("No data to export. Please apply filters first.")
            return
        
        # Get all unique keys from filtered data
        fieldnames = set()
        for record in self.filtered_data:
            fieldnames.update(record.keys())
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(self.filtered_data)
        
        print(f"Exported {len(self.filtered_data)} records to {filename}")


# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = [
        {"id": 1, "name": "Product A", "category": "Electronics", "price": 299.99, "created_at": "2024-01-15"},
        {"id": 2, "name": "Product B", "category": "Clothing", "price": 49.99, "created_at": "2024-02-20"},
        {"id": 3, "name": "Product C", "category": "Electronics", "price": 599.99, "created_at": "2024-01-10"},
        {"id": 4, "name": "Product D", "category": "Books", "price": 19.99, "created_at": "2024-03-05"},
        {"id": 5, "name": "Product E", "category": "Electronics", "price": 399.99, "created_at": "2024-02-01"},
    ]
    
    # Create filter instance
    filter_tool = DataExportFilter(sample_data)
    
    # Filter by date range (this will have issues due to the bug!)
    filtered = filter_tool.filter_by_date_range("2024-01-01", "2024-02-15")
    print(f"Found {len(filtered)} records in date range")
    
    # Export to CSV
    filter_tool.export_to_csv("filtered_export.csv")

