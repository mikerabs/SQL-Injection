import json
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import sys
import os

class DatabaseQueryTool:
    def __init__(self, config_path):
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)#load the JSON config file from the path specified in instantiation
        
        self.db_config = self.config['database_config']#all the config connection params stored here
        self.queries_config = self.config['queries']
        self.output_dir = "/app/output"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)#write the outputs of our malicious queries here
    
    def get_connection(self):
        """Create database connection"""
        try:
            connection = mysql.connector.connect(#unpacking config connection params
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database']
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def execute_query(self, query_config, test_case, use_prepared=False):
        """Execute query with given parameters"""
        connection = self.get_connection()
        if not connection:
            return None
        
        results = None
        error_message = None
        
        try:
            cursor = connection.cursor()
            
            # Build query
            table = query_config['table']
            key_column = query_config['key_column']
            columns = ", ".join(query_config['columns'])
            key_value = test_case['key_value']
            
            sql = f"SELECT {columns} FROM {table} WHERE {key_column} = {key_value}"#basic statement structure
            
            print(f"\n{'='*60}")
            print(f"Test Case: {test_case['name']}")
            print(f"Description: {test_case['description']}")
            print(f"Using Prepared Statement: {use_prepared}")
            print(f"Input key value: {repr(key_value)}")
            print(f"SQL Statement: {sql}")
            
            if use_prepared:
                # Using prepared statement
                sql_prepared = f"SELECT {columns} FROM {table} WHERE {key_column} = %s"
                print(f"Prepared SQL: {sql_prepared}")
                
                try:
                    cursor.execute(sql_prepared, (key_value,))
                    results = cursor.fetchall()
                    print("Prepared Statement Query executed successfully")
                except Error as e:
                    error_message = str(e)
                    print(f"Error with prepared statement: {error_message}")
            else:
                # Using vulnerable direct execution
                try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    print("Direct Query executed successfully (vulnerable)")
                except Error as e:
                    error_message = str(e)
                    print(f"SQL Error (expected for vulnerable): {error_message}")
            
            # Display results
            if results:
                print(f"\nResults ({len(results)} rows):")
                for row in results:
                    print(f"  {row}")
            elif not error_message:
                print("\nNo results returned")
            
            return {
                'test_case': test_case['name'],
                'use_prepared': use_prepared,
                'input': repr(key_value),
                'sql': sql,
                'error': error_message,
                'results': results,
                'row_count': len(results) if results else 0
            }
            
        except Exception as e:
            error_message = str(e)
            print(f"Unexpected error: {error_message}")
            return {
                'test_case': test_case['name'],
                'use_prepared': use_prepared,
                'input': repr(key_value),
                'sql': sql if 'sql' in locals() else 'N/A',
                'error': error_message,
                'results': None,
                'row_count': 0
            }
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def run_tests(self):
        """Run all test cases for both vulnerable and prepared statements"""
        query_config = self.queries_config['people_select']
        test_cases = query_config['test_cases']#specified within the JSON config
        
        all_results = []
        
        # Run vulnerable direct statements (use_prepared=False)
        print("\n" + "="*60)
        print("RUNNING VULNERABLE STATEMENTS (use_prepared=False)")
        print("="*60)#divider
        
        for test_case in test_cases:
            result = self.execute_query(query_config, test_case, use_prepared=False)
            all_results.append(result)
            
            # Save output to file
            self.save_output(result, "vulnerable")
        
        # Run prepared statements (use_prepared=True)
        print("\n" + "="*60)
        print("RUNNING PREPARED STATEMENTS (use_prepared=True)")
        print("="*60)
        
        for test_case in test_cases:
            result = self.execute_query(query_config, test_case, use_prepared=True)
            all_results.append(result)
            
            # Save output to file
            self.save_output(result, "prepared")
        
        return all_results
    
    def save_output(self, result, statement_type):
        """Save results to output file, format nicely"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{statement_type}_{result['test_case']}_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("="*60 + "\n")
            f.write(f"Test Case: {result['test_case']}\n")
            f.write(f"Statement Type: {'Prepared' if result['use_prepared'] else 'Vulnerable'}\n")
            f.write("-"*60 + "\n")
            f.write(f"Input Value: {result['input']}\n")
            f.write(f"SQL Statement: {result['sql']}\n")
            f.write(f"Error: {result['error'] if result['error'] else 'None'}\n")
            f.write(f"Rows Returned: {result['row_count']}\n")
            f.write("-"*60 + "\n")
            f.write("Results:\n")
            
            if result['results']:
                for row in result['results']:
                    f.write(f"  {row}\n")
            else:
                f.write("  No results\n")
            
            f.write("="*60 + "\n")
        
        print(f"Output saved to: {filepath}")
    
    def generate_summary_report(self, all_results):
        """Generate a summary report"""
        summary_path = os.path.join(self.output_dir, "summary_report.txt")
        
        with open(summary_path, 'w') as f: #Write to the summary file in /output
            f.write("SQL INJECTION TEST SUMMARY REPORT\n")
            f.write("="*60 + "\n\n")
            
            vulnerable_results = [r for r in all_results if not r['use_prepared']]
            prepared_results = [r for r in all_results if r['use_prepared']]
            
            f.write("VULNERABLE STATEMENTS:\n")
            f.write("-"*60 + "\n")
            for result in vulnerable_results:
                f.write(f"\nTest: {result['test_case']}\n")
                f.write(f"  Input: {result['input']}\n")
                f.write(f"  Success: {'No' if result['error'] else 'Yes'}\n")
                f.write(f"  Rows Returned: {result['row_count']}\n")
                if result['error']:
                    f.write(f"  Error: {result['error'][:100]}...\n")
            
            f.write("\n\nPREPARED STATEMENTS:\n")
            f.write("-"*60 + "\n")
            for result in prepared_results:
                f.write(f"\nTest: {result['test_case']}\n")
                f.write(f"  Input: {result['input']}\n")
                f.write(f"  Success: {'No' if result['error'] else 'Yes'}\n")
                f.write(f"  Rows Returned: {result['row_count']}\n")
                if result['error']:
                    f.write(f"  Error: {result['error'][:100]}...\n")
            
            f.write("\n\nCONCLUSIONS:\n")
            f.write("-"*60 + "\n")
            f.write("1. Vulnerable statements allow SQL injection attacks\n")
            f.write("2. Prepared statements prevent SQL injection\n")
            f.write("3. Always use prepared statements for user input\n")
        
        print(f"\nSummary report saved to: {summary_path}")

def main():
    # Check if config file exists
    config_path = "/app/config/config.json"
    
    if not os.path.exists(config_path):
        print(f"Config file not found at {config_path}")
        print("Looking in:", os.listdir("/app/config"))
        sys.exit(1)
    
    # Run the query tool class
    tool = DatabaseQueryTool(config_path) #Instantiate class instance
    all_results = tool.run_tests()#run tests method
    tool.generate_summary_report(all_results)#geerate a summary report on statements executed
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print(f"Check /app/output directory for results")
    print("="*60)

if __name__ == "__main__":
    main()
