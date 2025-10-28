def handle_devrc_command(self, tokens: List[str]):
        """Handle .devrc specific commands"""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token == '-out' and i + 1 < len(tokens):
                self.output_to_file(tokens[i + 1])
                i += 2
            
            elif token == '-crfolder' and i + 1 < len(tokens):
                self.create_folder(tokens[i + 1])
                i += 2
            
            elif token == '-pop':
                if i + 1 < len(tokens):
                    print(f"✓ Pop operation: {tokens[i + 1]}")
                i += 2
            
            elif token == '-plugin':
                print("✓ Plugin mode enabled")
                i += 1
            
            elif token == '-config':
                print("✓ Config mode enabled")
                i += 1
            
            elif token == '-c':
                print("✓ Compile mode enabled")
                i += 1
            
            elif token == '-timed':
                print("✓ Timed operation enabled")
                i += 1
            
            elif token == '-mode' and i + 1 < len(tokens):
                print(f"✓ Mode set to: {tokens[i + 1]}")
                i += 2
            
            elif token == '-force':
                print("✓ Force mode enabled")
                i += 1
            
            elif token == '-a':
                print("✓ Append operation")
                i += 1
            
            elif token == '-locate' and i + 1 < len(tokens):
                print(f"✓ Locate: {tokens[i + 1]}")
                i += 2
            
            elif token == '-to':
                print("✓ Transform operation")
                i += 1
            
            elif token == '-ext' and i + 1 < len(tokens):
                print(f"✓ Extension: {tokens[i + 1]}")
                i += 2
            
            elif token == '-cmdbin':
                print("✓ Command binary mode")
                i += 1
            
            elif token == '-cmdline':
                print("✓ Command line mode")
                i += 1
            
            elif token == '-rline' and i + 1 < len(tokens):
                print(f"✓ Run line: {tokens[i + 1]}")
                i += 2
            
    def handle_devrc_command(self, tokens: List[str]):
        """Handle .devrc specific commands"""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token == '-out' and i + 1 < len(tokens):
                self.output_to_file(tokens[i + 1])
                i += 2
            
            elif token == '-crfolder' and i + 1 < len(tokens):
                self.create_folder(tokens[i + 1])
                i += 2
            
            elif token == '-pop':
                if i + 1 < len(tokens):
                    print(f"✓ Pop operation: {tokens[i + 1]}")
                i += 2
            
            elif token == '-plugin':
                print("✓ Plugin mode enabled")
                i += 1
            
            elif token == '-config':
                print("✓ Config mode enabled")
                i += 1
            
            elif token == '-c':
                print("✓ Compile mode enabled")
                i += 1
            
            elif token == '-f':
                print("✓ Force file mode")
                i += 1
            
            elif token == '-timed':
                print("✓ Timed operation enabled")
                i += 1
            
            elif token == '-mode' and i + 1 < len(tokens):
                print(f"✓ Mode set to: {tokens[i + 1]}")
                i += 2
            
            elif token == '-force':
                print("✓ Force mode enabled")
                i += 1
            
            elif token == '-a':
                print("✓ Append operation")
                i += 1
            
            elif token == '-locate' and i + 1 < len(tokens):
                print(f"✓ Locate: {tokens[i + 1]}")
                i += 2
            
            elif token == '-to':
                print("✓ Transform operation")
                i += 1
            
            elif token == '-ext' and i + 1 < len(tokens):
                print(f"✓ Extension: {tokens[i + 1]}")
                i += 2
            
            elif token == '-cmdbin':
                print("✓ Command binary mode")
                i += 1
            
            elif token == '-cmdline':
                print("✓ Command line mode")
                i += 1
            
            elif token == '-rline' and i + 1 < len(tokens):
                print(f"✓ Run line: {tokens[i + 1]}")
                i += 2
            
            elif token == '-r' and i + 1 < len(tokens):
                print(f"✓ Run mode: {tokens[i + 1]}")
                i += 2
            
            elif token == '-byp':
                print("✓ Bypass mode enabled")
                i += 1
            
            elif token == '-h' and i + 1 < len(tokens):
                print(f"✓ Handle pattern: {tokens[i + 1]}")
                i += 2
            
            elif token == '-ch':
                print("✓ Chain operation")
                i += 1
            
            elif token == '-numline':
                print("✓ Number line mode")
                i += 1
            
            elif token == '-ff':
                print("✓ Fast forward mode")
                i += 1
            
            elif token == '-glob' and i + 1 < len(tokens):
                print(f"✓ Glob pattern: {tokens[i + 1]}")
                i += 2
            
            elif token == '-set':
                print("✓ Set operation")
                i += 1
            
            elif token == '-getline':
                print("✓ Get line operation")
                i += 1
            
            elif token == '-linenum':
                print("✓ Line number operation")
                i += 1
            
            elif token == '-activeline':
                print("✓ Active line mode")
                i += 1
            
            elif token == '-enable':
                print("✓ Enable flag")
                i += 1
            
            elif token == '-commitline':
                print("✓ Commit line operation")
                i += 1
            
            elif token == '-usr':
                print("✓ User mode")
                i += 1
            
            elif token == '-active':
                print("✓ Active mode")
                i += 1
            
            elif token == '-o' and i + 1 < len(tokens):
                print(f"✓ Or operation: {tokens[i + 1]}")
                i += 2
            
            elif token == '-exclude' and i + 1 < len(tokens):
                print(f"✓ Exclude: {tokens[i + 1]}")
                i += 2
            
            elif token == '-expotag':
                print("✓ Export tag")
                i += 1
            
            elif token == '-add':
                print("✓ Add operation")
                i += 1
            
            elif token == '-rm':
                print("✓ Remove operation")
                i += 1
            
            elif token == '-replace':
                print("✓ Replace operation")
                i += 1
            
            elif token == '-pub':
                print("✓ Publish mode")
                i += 1
            
            elif token == '-proc':
                print("✓ Process mode")
                i += 1
            
            elif token == '-currentline':
                print("✓ Current line mode")
                i += 1
            
            elif token == '-reg':
                print("✓ Register mode")
                i += 1
            
            elif token == '-file_ext':
                print("✓ File extension mode")
                i += 1
            
            elif token == '-setglob':
                print("✓ Set glob mode")
                i += 1
            
            elif token == '-op':
                print("✓ Operation mode")
                i += 1
            
            elif token == '-math':
                print("✓ Math mode")
                i += 1
            
            else:
                i += 1#!/usr/bin/env python3
"""
DevRC DSL Interpreter
Parses and executes .devrc configuration files
"""

import re
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional


class DevRCInterpreter:
    def __init__(self):
        self.variables = {}
        self.sections = {}
        self.section_types = {}
        self.current_section = None
        self.imported_files = set()
        self.import_stack = []
        self.environments = {}
        self.active_environment = None
        self.root_dir = os.getcwd()
        
    def parse_file(self, filepath: str) -> Dict[str, List[str]]:
        """Parse a .devrc file into sections"""
        # Prevent circular imports
        abs_path = os.path.abspath(filepath)
        if abs_path in self.import_stack:
            print(f"✗ Circular import detected: {filepath}")
            return {}
        
        self.import_stack.append(abs_path)
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        sections = {}
        current_section = None
        current_type = None
        
        for line in content.split('\n'):
            original_line = line
            
            # Check for environment activation BEFORE removing comments
            if line.strip().startswith('#[') and ']/ACTIVATE' in line:
                self.handle_environment_activation(line.strip())
                continue
            
            # Check for inline imports with @DEVRC.IMPORT=
            if '@DEVRC.IMPORT=' in line:
                self.handle_inline_import(line)
                # Don't skip the line, let it be processed
            
            # Remove comments (but not environment markers)
            if '#' in line and not line.strip().startswith('#['):
                line = line.split('#')[0]
            
            line = line.strip()
            if not line:
                continue
            
            # Check for imports
            if line.startswith('@DEVRC.IMPORT.'):
                self.handle_import(line, os.path.dirname(filepath))
                continue
            
            # Check for type annotations
            if line.startswith('@[') and line.endswith(']'):
                current_type = line[2:-1]
                print(f"✓ Type annotation found: {current_type}")
                continue
                
            # Check for section headers
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                sections[current_section] = []
                if current_type:
                    self.section_types[current_section] = current_type
                    current_type = None
            elif current_section:
                sections[current_section].append(line)
        
        self.import_stack.pop()
        return sections
    
    def tokenize(self, line: str) -> List[str]:
        """Tokenize a line into components"""
        # Handle quoted strings
        tokens = []
        current = []
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
                current.append(char)
            elif char in [' ', '\t'] and not in_quotes:
                if current:
                    tokens.append(''.join(current))
                    current = []
            else:
                current.append(char)
        
        if current:
            tokens.append(''.join(current))
        
        return tokens
    
    def parse_assignment(self, line: str) -> Optional[tuple]:
        """Parse variable assignment"""
        if '=' in line:
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            var_value = parts[1].strip()
            return (var_name, var_value)
        return None
    
    def evaluate_expression(self, expr: str) -> Any:
        """Evaluate an expression"""
        expr = expr.strip()
        
        # Remove quotes
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        
        # Check if it's a variable reference
        if expr in self.variables:
            return self.variables[expr]
        
        # Check for boolean literals
        if expr.lower() in ['true', '-true']:
            return True
        if expr.lower() in ['false', '-false']:
            return False
        
        # Check for null
        if expr.lower() == 'null':
            return None
        
        return expr
    
    def handle_import(self, line: str, base_path: str):
        """Handle @DEVRC.IMPORT.[variablename] statements"""
        # Parse import statement: @DEVRC.IMPORT.[variablename] or @DEVRC.IMPORT.[variablename]="path"
        match = re.match(r'@DEVRC\.IMPORT\.(\w+)(?:="?([^"]+)"?)?', line)
        if not match:
            print(f"✗ Invalid import syntax: {line}")
            return
        
        var_name = match.group(1)
        import_path = match.group(2)
        
        # If no path specified, check if variable exists
        if not import_path:
            if var_name not in self.variables:
                print(f"✗ Import failed: variable '{var_name}' not defined")
                return
            import_path = self.variables[var_name]
        
        # Resolve relative paths
        if not os.path.isabs(import_path):
            import_path = os.path.join(base_path, import_path)
        
        # Check if already imported
        abs_import_path = os.path.abspath(import_path)
        if abs_import_path in self.imported_files:
            print(f"✓ Already imported: {import_path}")
            return
        
        # Check if file exists
        if not os.path.exists(import_path):
            print(f"✗ Import file not found: {import_path}")
            return
        
        print(f"✓ Importing from: {import_path}")
        self.imported_files.add(abs_import_path)
        
        # Parse and merge the imported file
        imported_sections = self.parse_file(import_path)
        for section_name, lines in imported_sections.items():
            if section_name in self.sections:
                # Merge with existing section
                print(f"  ↳ Merging section: [{section_name}]")
                self.sections[section_name].extend(lines)
            else:
                # Add new section
                print(f"  ↳ Adding section: [{section_name}]")
                self.sections[section_name] = lines
                # Copy type if exists
                if section_name in self.section_types:
                    self.section_types[section_name] = self.section_types[section_name]
    
    def handle_inline_import(self, line: str):
        """Handle inline @DEVRC.IMPORT= statements within expressions"""
        # Parse: @DEVRC.IMPORT="./file.devrc" or @DEVRC.IMPORT="dirlist"
        match = re.search(r'@DEVRC\.IMPORT="([^"]+)"', line)
        if match:
            import_ref = match.group(1)
            print(f"✓ Inline import reference: {import_ref}")
            
            # Store as variable for later use
            if 'is STR' in line:
                var_match = re.search(r'is STR "([^"]+)"', line)
                if var_match:
                    var_name = var_match.group(1)
                    self.variables[var_name] = import_ref
                    print(f"  ↳ Stored as: {var_name}")
    
    def handle_environment_activation(self, line: str):
        """Handle #[environmentname]/ACTIVATE directives"""
        # Parse: #[environmentname]/ACTIVATE
        match = re.match(r'#\[([^\]]+)\]/ACTIVATE', line)
        if not match:
            print(f"✗ Invalid environment activation syntax: {line}")
            return
        
        env_name = match.group(1)
        
        # Create environment directory path from root
        env_path = os.path.join(self.root_dir, env_name)
        
        # Create environment if it doesn't exist
        if not os.path.exists(env_path):
            try:
                os.makedirs(env_path, exist_ok=True)
                print(f"✓ Created environment directory: {env_path}")
            except Exception as e:
                print(f"✗ Failed to create environment directory: {e}")
                return
        
        # Activate the environment
        self.active_environment = env_name
        self.environments[env_name] = {
            'path': env_path,
            'root': self.root_dir,
            'activated_at': os.getcwd(),
            'mode': 'SCRIPT',
            'exported': {},
            'subenv': {},
            'content': {}
        }
        
        # Set environment variable
        self.variables['env'] = env_name
        self.variables['activate'] = f"{env_name}/ACTIVATE"
        self.variables['currentdir'] = env_path
        
        # Change to environment directory
        try:
            os.chdir(env_path)
            print(f"✓ Environment activated: {env_name}")
            print(f"  ↳ Working directory: {env_path}")
            print(f"  ↳ Root directory: {self.root_dir}")
            print(f"  ↳ Mode: SCRIPT")
        except Exception as e:
            print(f"✗ Failed to change to environment directory: {e}")
    
    def create_folder(self, path: str):
        """Create a folder if it doesn't exist"""
        path = path.strip('"').replace('*', '')
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            print(f"✓ Created folder: {path}")
        except Exception as e:
            print(f"✗ Error creating folder {path}: {e}")
    
    def output_to_file(self, path: str, content: Any = None):
        """Handle output to file"""
        path = path.strip('"').replace('*', '')
        try:
            if '*' in path or path.endswith('/'):
                # Directory output
                Path(path).mkdir(parents=True, exist_ok=True)
                print(f"✓ Prepared output directory: {path}")
            else:
                # File output
                Path(path).parent.mkdir(parents=True, exist_ok=True)
                if content:
                    with open(path, 'w') as f:
                        if isinstance(content, dict):
                            json.dump(content, f, indent=2)
                        else:
                            f.write(str(content))
                print(f"✓ Output to: {path}")
        except Exception as e:
            print(f"✗ Error outputting to {path}: {e}")
    
    def execute_command(self, command: List[str]):
        """Execute a system command"""
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print(f"✓ Executed: {' '.join(command)}")
            return result.stdout
        except Exception as e:
            print(f"✗ Error executing command: {e}")
            return None
    
    def process_line(self, line: str):
        """Process a single line of DevRC code"""
        tokens = self.tokenize(line)
        if not tokens:
            return
        
        # Handle special comment directives (xcn-byp)
        if line.strip().startswith('#xcn-byp'):
            self.handle_xcn_bypass(line)
            return
        
        # Handle assignments with special syntax
        assignment = self.parse_assignment(line)
        if assignment:
            var_name, var_value = assignment
            
            # Handle special assignments like poot={}
            if var_value.strip() in ['{}', '[]']:
                self.variables[var_name] = {}
                print(f"✓ Initialized {var_name} as empty container")
                return
            
            # Handle complex assignments with try()
            if 'try (' in var_value:
                self.handle_try_assignment(var_name, var_value)
                return
            
            # Handle function assignments
            if var_value.strip().startswith('function ('):
                self.handle_function_assignment(var_name, var_value)
                return
            
            self.variables[var_name] = self.evaluate_expression(var_value)
            print(f"✓ Set {var_name} = {self.variables[var_name]}")
            return
        
        # Handle dirlist with -glob
        if tokens[0] == 'dirlist' or 'dirlist=' in line:
            self.handle_dirlist(line)
            return
        
        # Handle currentdir
        if tokens[0] == 'currentdir' or 'currentdir=' in line:
            self.handle_currentdir(line)
            return
        
        # Handle subenv
        if tokens[0] == 'subenv' or 'subenv=' in line:
            self.handle_subenv(line)
            return
        
        # Handle prod/dev/debug environments
        if tokens[0] in ['prod', 'dev', 'debug'] and '=' in line:
            self.handle_environment_category(line)
            return
        
        # Handle linenum
        if tokens[0] == 'linenum' or 'linenum=' in line:
            self.handle_linenum(line)
            return
        
        # Handle current with activeline
        if tokens[0] == 'current' or 'current=' in line:
            self.handle_current_line(line)
            return
        
        # Handle func assignments
        if tokens[0] == 'func' or 'func=' in line:
            self.handle_func_assignment(line)
            return
        
        # Handle math operations
        if tokens[0] == 'math' or 'math=' in line:
            self.handle_math_operation(line)
            return
        
        # Handle number operations
        if tokens[0] == 'number' or 'number=' in line:
            self.handle_number_operation(line)
            return
        
        # Handle row/column operations
        if tokens[0] in ['row', 'column'] or 'row=' in line or 'column=' in line:
            self.handle_row_column(line)
            return
        
        # Handle position operations
        if tokens[0] == 'position' or 'position=' in line:
            self.handle_position(line)
            return
        
        # Handle dgl operations
        if tokens[0] == 'dgl' or 'dgl=' in line:
            self.handle_dgl(line)
            return
        
        # Handle object operations
        if tokens[0] == 'object' or 'object=' in line:
            self.handle_object_operation(line)
            return
        
        # Handle draw operations
        if tokens[0] == 'draw' or 'draw=' in line:
            self.handle_draw_operation(line)
            return
        
        # Handle scene operations
        if tokens[0] == 'scene' or 'scene=' in line:
            self.handle_scene_operation(line)
            return
        
        # Handle -math operations
        if '-math' in line:
            self.handle_math_flag(line)
            return
        
        # Handle eq (equations)
        if tokens[0] == 'eq' or 'eq=' in line:
            self.handle_equation(line)
            return
        
        # Handle coordinate operations (x, y, z)
        if tokens[0] in ['x', 'y', 'z', 'L'] and '=' in line:
            self.handle_coordinate(line)
            return
        
        # Handle abs operations
        if 'abs.' in line:
            self.handle_abs_operation(line)
            return
        
        # Handle cos/sin operations
        if 'cos.' in line or 'sin.' in line:
            self.handle_trig_operation(line)
            return
        
        # Handle prime notation (x[prime])
        if '[prime]' in line:
            self.handle_prime_notation(line)
            return
        
        # Handle tokenlist
        if 'tokenlist' in tokens[0]:
            self.handle_tokenlist(line)
            return
        
        # Handle keyword
        if tokens[0] == 'keyword' or 'keyword=' in line:
            self.handle_keyword(line)
            return
        
        # Handle var with tokenlist
        if tokens[0] == 'var' and 'tokenlist' in line:
            self.handle_var_tokenlist(line)
            return
        
        # Handle input operations
        if tokens[0] == 'input' or 'input=' in line:
            self.handle_input(line)
            return
        
        # Handle err assignments
        if tokens[0] == 'err' or 'err=' in line:
            self.handle_err(line)
            return
        
        # Handle COCOHOWTO
        if 'COCOHOWTO' in tokens[0]:
            self.handle_cocohowto(line)
            return
        
        # Handle function definitions
        if tokens[0] == 'function':
            self.handle_function_definition(line)
            return
        
        # Handle return statements
        if tokens[0] == 'return':
            self.handle_return_statement(line)
            return
        
        # Handle export statements
        if tokens[0] == 'export':
            self.handle_export_statement(line)
            return
        
        # Handle -r debug export
        if tokens[0] == '-r' and len(tokens) > 1 and tokens[1] == 'debug' and 'export' in line:
            self.handle_debug_export(line)
            return
        
        # Handle activate keyword
        if tokens[0] == 'activate':
            self.handle_activate_keyword(line)
            return
        
        # Handle catch blocks
        if tokens[0] == 'catch':
            self.handle_catch_block(line)
            return
        
        # Handle .devrc commands
        if tokens[0] == '.devrc':
            self.handle_devrc_command(tokens[1:])
        
        # Handle if statements
        elif tokens[0] == 'if':
            self.handle_if_statement(line)
        
        # Handle for loops
        elif tokens[0] == 'for':
            self.handle_for_loop(line)
        
        # Handle do statements
        elif tokens[0] == 'do':
            self.handle_do_statement(tokens[1:])
        
        # Handle out command
        elif tokens[0] == 'out':
            if len(tokens) > 1:
                self.output_to_file(tokens[1])
        
        # Handle get operations
        elif tokens[0] == 'get':
            self.handle_get_operation(line)
        
        # Handle in operations  
        elif tokens[0] == 'in':
            self.handle_in_operation(line)
        
        # Handle try blocks
        elif tokens[0] == 'try':
            self.handle_try_block(line)
        
        # Handle else statements
        elif tokens[0] == 'else':
            self.handle_else_statement(line)
    
    def handle_function_definition(self, line: str):
        """Handle function definitions"""
        match = re.search(r'function\s+(\w+)\s*\(', line)
        if match:
            func_name = match.group(1)
            print(f"✓ Function defined: {func_name}")
            self.variables[func_name] = "function"
        else:
            # Anonymous function or function call syntax
            print(f"✓ Function block defined")
    
    def handle_return_statement(self, line: str):
        """Handle return statements"""
        # Extract return value
        match = re.search(r'return\s+(.+)', line)
        if match:
            return_val = match.group(1).strip()
            print(f"✓ Return: {return_val}")
            if self.active_environment:
                self.environments[self.active_environment]['return_value'] = return_val
    
    def handle_export_statement(self, line: str):
        """Handle export statements for environment variables"""
        # Parse: export name ( ... )
        match = re.search(r'export\s+(\w+)\s*\(', line)
        if match:
            export_name = match.group(1)
            print(f"✓ Export: {export_name}")
            
            if self.active_environment:
                env_data = self.environments[self.active_environment]
                if 'exported' not in env_data:
                    env_data['exported'] = {}
                env_data['exported'][export_name] = line
                
                # Handle special exports
                if export_name == 'byp':
                    self.handle_bypass_export(line)
                elif export_name == 'env':
                    self.handle_env_export(line)
    
    def handle_activate_keyword(self, line: str):
        """Handle activate= keyword for activation mode"""
        if '-mode SCRIPT' in line:
            print(f"✓ Activate mode: SCRIPT")
            if self.active_environment:
                self.environments[self.active_environment]['mode'] = 'SCRIPT'
    
    def handle_bypass_export(self, line: str):
        """Handle bypass export for command execution"""
        print(f"✓ Bypass export configured")
        
        # Extract file patterns
        if '.py' in line:
            print(f"  ↳ Python file execution enabled")
        if 'terminal' in line:
            print(f"  ↳ Terminal mode enabled")
        if '-cmdbin' in line:
            print(f"  ↳ Command binary mode enabled")
        if '-byp' in line:
            print(f"  ↳ Bypass flag set")
    
    def handle_env_export(self, line: str):
        """Handle environment export"""
        print(f"✓ Environment export configured")
        if self.active_environment:
            env_name = self.active_environment
            print(f"  ↳ Exporting environment: {env_name}")
    
    def handle_func_assignment(self, line: str):
        """Handle func=function() assignments"""
        print(f"✓ Function assignment")
        
        if 'return table[content]' in line:
            print(f"  ↳ Returns table content")
        
        self.variables['func'] = 'function'
    
    def handle_tokenlist(self, line: str):
        """Handle tokenlist operations and specifications"""
        print(f"✓ Tokenlist operation")
        
        # Handle tokenlist.spec.equalsign
        if 'tokenlist.spec.equalsign' in line:
            match = re.search(r'tokenlist\.spec\.equalsign="([^"]+)"', line)
            if match:
                token = match.group(1)
                print(f"  ↳ Token spec equals sign: {token}")
                self.variables['tokenlist.spec.equalsign'] = token
        
        # Handle tokenlist.spec."*"
        if 'tokenlist.spec."*"' in line:
            print(f"  ↳ Token spec wildcard")
        
        # Handle tokenlist content array
        if 'content[' in line:
            # Extract token array
            match = re.search(r'content\[([^\]]+)\]', line)
            if match:
                tokens_str = match.group(1)
                print(f"  ↳ Token content: {tokens_str}")
                self.variables['tokenlist'] = tokens_str
        
        # Handle -exclude
        if '-exclude' in line:
            exclude_match = re.search(r'-exclude "([^"]+)"', line)
            if exclude_match:
                print(f"  ↳ Excluding: {exclude_match.group(1)}")
    
    def handle_keyword(self, line: str):
        """Handle keyword definitions"""
        print(f"✓ Keyword definition")
        
        match = re.search(r'keyword="([^"]*)"', line)
        if match:
            keyword = match.group(1)
            self.variables['keyword'] = keyword
            print(f"  ↳ Keyword: '{keyword}'")
    
    def handle_var_tokenlist(self, line: str):
        """Handle var with tokenlist and catch"""
        print(f"✓ Variable with tokenlist")
        
        if 'catch' in line:
            print(f"  ↳ With catch block")
        
        if 'tokenlist.spec.equalsign' in line:
            print(f"  ↳ Using tokenlist equals sign spec")
        
        if 'keyword' in line:
            print(f"  ↳ With keyword reference")
    
    def handle_input(self, line: str):
        """Handle input operations"""
        print(f"✓ Input operation")
        
        if '-usr' in line:
            print(f"  ↳ User input mode")
        
        if '-active' in line:
            print(f"  ↳ Active input")
        
        if 'INPUT:' in line:
            print(f"  ↳ Input prompt: INPUT:")
        
        if '-cmdbin -cmdline' in line:
            print(f"  ↳ Command line input")
        
        self.variables['input'] = ''
    
    def handle_err(self, line: str):
        """Handle error assignments"""
        print(f"✓ Error handling")
        
        if 'is false' in line:
            print(f"  ↳ Error set to false")
            self.variables['err'] = False
        
        if '-o null' in line:
            print(f"  ↳ Or null")
        
        if 'with var -o func' in line:
            print(f"  ↳ With var or func")
    
    def handle_cocohowto(self, line: str):
        """Handle COCOHOWTO references"""
        print(f"✓ COCOHOWTO operation")
        
        if '@DEVRC.IMPORT.COCOHOWTO' in line:
            print(f"  ↳ Importing COCOHOWTO")
        
        if 'file, filename, file_ext' in line:
            print(f"  ↳ With file parameters")
    
    def handle_debug_export(self, line: str):
        """Handle -r debug export blocks"""
        print(f"✓ Debug export")
        
        # Extract this.* references
        this_refs = re.findall(r'this\.(\w+(?:\.\w+)*)', line)
        if this_refs:
            print(f"  ↳ This references: {', '.join(this_refs)}")
        
        # Handle -enable
        if '-enable' in line:
            print(f"  ↳ Enable flag set")
        
        # Handle catch blocks
        if 'catch {' in line:
            print(f"  ↳ With catch block")
        
        # Handle return statements
        if 'return {' in line:
            print(f"  ↳ With return block")
        
        # Handle -expotag
        if '-expotag' in line:
            print(f"  ↳ Export tag enabled")
    
    def handle_catch_block(self, line: str):
        """Handle catch blocks for error handling"""
        print(f"✓ Catch block")
        
        # Extract catch content
        match = re.search(r'catch\s*{([^}]+)}', line)
        if match:
            catch_content = match.group(1).strip()
            print(f"  ↳ Catch: {catch_content[:50]}...")
        
        # Handle err in STR
        if 'err in STR' in line:
            print(f"  ↳ Error as string")
        
        # Handle exceptions
        if 'exceptions' in line:
            print(f"  ↳ Exception handling")
    
    def handle_else_statement(self, line: str):
        """Handle else statements with try/catch"""
        print(f"✓ Else statement")
        
        if 'try (' in line:
            print(f"  ↳ With try block")
        
        if 'catch' in line:
            print(f"  ↳ With catch block")
    
    def handle_function_assignment(self, var_name: str, var_value: str):
        """Handle function assignments like var=function()"""
        print(f"✓ Function assigned to: {var_name}")
        self.variables[var_name] = 'function'
    
    def handle_xcn_bypass(self, line: str):
        """Handle #xcn-byp special bypass directives"""
        print(f"✓ XCN Bypass directive")
        
        # Extract directive name
        match = re.match(r'#xcn-byp-([^\s]+)', line)
        if match:
            directive = match.group(1)
            print(f"  ↳ Directive: {directive}")
        
        # Handle return blocks
        if 'return {' in line:
            print(f"  ↳ With return block")
        
        # Handle section references
        if '[COCO.HOWTO.COMPILE]' in line:
            print(f"  ↳ Section reference: COCO.HOWTO.COMPILE")
        
        # Handle this.lines.fetched
        if 'this.lines.fetched' in line:
            print(f"  ↳ Fetching lines")
    
    def handle_math_operation(self, line: str):
        """Handle mathematical operations"""
        print(f"✓ Math operation")
        
        if '-add' in line:
            print(f"  ↳ Addition operation")
        
        if 'table[content]' in line:
            print(f"  ↳ With table content")
        
        if 'this table[content]' in line:
            print(f"  ↳ This table reference")
        
        if 'in numerics' in line:
            print(f"  ↳ Numeric context")
        
        self.variables['math'] = 'math_operation'
    
    def handle_number_operation(self, line: str):
        """Handle number operations"""
        print(f"✓ Number operation")
        
        # Extract numeric values
        numbers = re.findall(r'in STR "(\d)"', line)
        if numbers:
            print(f"  ↳ Numbers: {', '.join(numbers)}")
        
        if '-r debug' in line:
            print(f"  ↳ Debug mode")
        
        if 'with math' in line:
            print(f"  ↳ With math context")
        
        self.variables['number'] = 'number_value'
    
    def handle_row_column(self, line: str):
        """Handle row and column operations"""
        op_type = 'row' if 'row' in line else 'column'
        print(f"✓ {op_type.capitalize()} operation")
        
        if '-c numeric' in line:
            print(f"  ↳ Compile numeric")
        
        if '-rm row' in line:
            print(f"  ↳ Remove row")
        
        if 'in column' in line:
            print(f"  ↳ In column context")
        
        if 'get "row"' in line:
            print(f"  ↳ Get row")
        
        if 'this.script.math' in line:
            print(f"  ↳ Script math reference")
        
        self.variables[op_type] = f'{op_type}_data'
    
    def handle_position(self, line: str):
        """Handle position operations"""
        print(f"✓ Position operation")
        
        if '-replace' in line:
            print(f"  ↳ Replace operation")
        
        if 'new number' in line:
            print(f"  ↳ New number")
        
        if 'with STR is row' in line:
            print(f"  ↳ With row string")
        
        self.variables['position'] = 'position_data'
    
    def handle_dgl(self, line: str):
        """Handle dgl (digital/data general) operations"""
        print(f"✓ DGL operation")
        
        if '-pub' in line:
            print(f"  ↳ Publish mode")
        
        if '-pop' in line:
            print(f"  ↳ Pop operation")
        
        if 'get -force' in line:
            print(f"  ↳ Force get")
        
        self.variables['dgl'] = 'dgl_data'
    
    def handle_object_operation(self, line: str):
        """Handle object operations for 3D scene management"""
        print(f"✓ Object operation")
        
        # Handle object assignment
        if 'object=' in line:
            if 'this.script' in line:
                print(f"  ↳ From script")
            
            if '{new object' in line:
                print(f"  ↳ New object creation")
        
        # Handle object.name
        if 'object.name=' in line:
            match = re.search(r'object\.name="([^"]+)"', line)
            if match:
                name = match.group(1)
                print(f"  ↳ Object name: {name}")
                self.variables['object.name'] = name
        
        # Handle file operations
        if '-to -c file_ext' in line:
            print(f"  ↳ To file extension")
        
        if 'with STR file_name' in line:
            print(f"  ↳ With filename")
        
        # Handle .thr file type
        if '.thr' in line:
            print(f"  ↳ THR file format")
        
        self.variables['object'] = 'object_instance'
    
    def handle_draw_operation(self, line: str):
        """Handle draw operations for rendering"""
        print(f"✓ Draw operation")
        
        # Extract draw target
        if 'draw (' in line or 'draw(' in line:
            match = re.search(r'draw\s*\("([^"]+)"\)', line)
            if match:
                target = match.group(1)
                print(f"  ↳ Drawing: {target}")
        
        if 'new object' in line:
            print(f"  ↳ New object")
        
        if 'in scene' in line:
            print(f"  ↳ In scene context")
        
        if '-currentline' in line:
            print(f"  ↳ Current line mode")
        
        if 'with math' in line:
            print(f"  ↳ With mathematics")
        
        self.variables['draw'] = 'draw_operation'
    
    def handle_scene_operation(self, line: str):
        """Handle scene operations for 3D scenes"""
        print(f"✓ Scene operation")
        
        if 'scene={' in line:
            print(f"  ↳ Scene initialization")
        
        if 'new object' in line:
            print(f"  ↳ Adding new object")
        
        if 'with eq' in line:
            print(f"  ↳ With equation")
        
        if 'do table[content]' in line:
            print(f"  ↳ Execute table content")
        
        if '-out file_ext' in line:
            print(f"  ↳ Output to file")
        
        self.variables['scene'] = 'scene_data'
    
    def handle_math_flag(self, line: str):
        """Handle -math flag operations"""
        print(f"✓ Math flag operation")
        
        if '-math -op' in line:
            print(f"  ↳ Math operator")
        
        if '-math -mode' in line:
            print(f"  ↳ Math mode")
        
        if 'max=math' in line:
            print(f"  ↳ Maximum operation")
        
        if '-math eq=' in line:
            print(f"  ↳ Math equation")
    
    def handle_equation(self, line: str):
        """Handle equation definitions"""
        print(f"✓ Equation operation")
        
        if 'eq= function' in line:
            print(f"  ↳ Function-based equation")
        
        if 'eq= is scene' in line:
            print(f"  ↳ Scene equation")
        
        if 'abs.x' in line or 'abs.y' in line or 'abs.z' in line:
            print(f"  ↳ Absolute value operations")
        
        if 'cos.' in line or 'sin.' in line:
            print(f"  ↳ Trigonometric operations")
        
        self.variables['eq'] = 'equation'
    
    def handle_coordinate(self, line: str):
        """Handle x, y, z coordinate operations"""
        coord_match = re.match(r'^\s*([xyzL])\s*=', line)
        if coord_match:
            coord = coord_match.group(1)
            print(f"✓ Coordinate {coord} operation")
            
            # Extract value
            value_match = re.search(r'=\s*(-?\d+(?:\.\d+)?)', line)
            if value_match:
                value = value_match.group(1)
                print(f"  ↳ Value: {value}")
                self.variables[coord] = value
        
        # Handle max coordinates
        if 'max.' in line:
            max_match = re.search(r'max\.([xyz])\s*=\s*(.+)', line)
            if max_match:
                coord = max_match.group(1)
                print(f"  ↳ Max {coord} coordinate")
    
    def handle_abs_operation(self, line: str):
        """Handle absolute value operations"""
        print(f"✓ Absolute value operation")
        
        if 'abs.x' in line or 'abs.y' in line or 'abs.z' in line:
            abs_var = re.search(r'abs\.([xyz])', line)
            if abs_var:
                print(f"  ↳ Absolute {abs_var.group(1)}")
    
    def handle_trig_operation(self, line: str):
        """Handle trigonometric operations"""
        print(f"✓ Trigonometric operation")
        
        if 'cos.' in line:
            trig_match = re.search(r'cos\.(\w+)', line)
            if trig_match:
                var = trig_match.group(1)
                print(f"  ↳ Cosine of {var}")
        
        if 'sin.' in line:
            trig_match = re.search(r'sin\.(\w+)', line)
            if trig_match:
                var = trig_match.group(1)
                print(f"  ↳ Sine of {var}")
        
        # Handle special values
        if 'zero' in line or 'ninety' in line or 'one_hundred_eighty' in line:
            print(f"  ↳ Special angle value")
    
    def handle_prime_notation(self, line: str):
        """Handle prime notation for transformed coordinates"""
        print(f"✓ Prime notation (transformed coordinate)")
        
        prime_vars = re.findall(r'([xyz])\[prime\]', line)
        if prime_vars:
            for var in prime_vars:
                print(f"  ↳ {var}' (transformed {var})")
        
        # Handle transformation operations
        if '*' in line or '+' in line or '-' in line:
            print(f"  ↳ Coordinate transformation")
        """Handle try blocks"""
        # Extract content in try(...)
        match = re.search(r'try\s*\((.+)\)', line, re.DOTALL)
        if match:
            try_content = match.group(1).strip()
            print(f"✓ Try block: {try_content[:50]}...")
            # Process the content inside try
            self.process_line(try_content)
    
    def handle_try_assignment(self, var_name: str, var_value: str):
        """Handle assignments with try() blocks"""
        match = re.search(r'try\s*\((.+)\)', var_value)
        if match:
            content = match.group(1).strip()
            self.variables[var_name] = content
            print(f"✓ Set {var_name} with try block: {content}")
    
    def handle_dirlist(self, line: str):
        """Handle dirlist with -glob syntax"""
        print(f"✓ Directory list operation")
        
        # Extract glob pattern
        if '-glob default' in line:
            print(f"  ↳ Using default glob pattern")
        
        # Extract output
        if '-out' in line:
            match = re.search(r'-out "([^"]+)"', line)
            if match:
                output = match.group(1)
                print(f"  ↳ Output to: {output}")
        
        # Handle inline import
        if '@DEVRC.IMPORT=' in line:
            print(f"  ↳ With import reference")
        
        # Set variable
        self.variables['dirlist'] = "./"
        
    def handle_currentdir(self, line: str):
        """Handle currentdir = dirlist './' this.dir"""
        print(f"✓ Current directory operation")
        
        if 'this.dir' in line:
            print(f"  ↳ Using this.dir reference")
        
        current_dir = self.variables.get('currentdir', os.getcwd())
        self.variables['currentdir'] = current_dir
        print(f"  ↳ Current dir: {current_dir}")
    
    def handle_subenv(self, line: str):
        """Handle subenv = env.category"""
        print(f"✓ Sub-environment configuration")
        
        if 'env.category' in line:
            if self.active_environment:
                env_data = self.environments[self.active_environment]
                env_data['subenv'] = {'category': 'default'}
                print(f"  ↳ Sub-environment category set")
    
    def handle_environment_category(self, line: str):
        """Handle prod/dev/debug environment categories"""
        # Parse: prod=drizzle[content+subenv=["debug","prod","dev"]]
        match = re.match(r'(\w+)=(\w+)\[(.+)\]', line)
        if match:
            category = match.group(1)
            env_name = match.group(2)
            content = match.group(3)
            
            print(f"✓ Environment category: {category}")
            print(f"  ↳ Environment: {env_name}")
            
            # Parse subenv array
            if 'subenv=' in content:
                subenv_match = re.search(r'subenv=\[([^\]]+)\]', content)
                if subenv_match:
                    subenvs = [s.strip('"') for s in subenv_match.group(1).split(',')]
                    print(f"  ↳ Sub-environments: {', '.join(subenvs)}")
                    
                    if self.active_environment:
                        env_data = self.environments[self.active_environment]
                        env_data['categories'] = subenvs
    
    def handle_linenum(self, line: str):
        """Handle linenum = this.lines.fetched (-out is numerics)"""
        print(f"✓ Line number operation")
        
        if 'this.lines.fetched' in line:
            print(f"  ↳ Fetching line numbers")
        
        if '-out is numerics' in line:
            print(f"  ↳ Output as numerics")
        
        self.variables['linenum'] = 0
    
    def handle_current_line(self, line: str):
        """Handle current line with -activeline"""
        print(f"✓ Current line operation")
        
        if '-linenum' in line:
            print(f"  ↳ Using line numbers")
        
        if '-getline' in line:
            print(f"  ↳ Getting line content")
        
        if '-activeline' in line:
            print(f"  ↳ Active line mode enabled")
        
        if 'currentdir' in line:
            print(f"  ↳ From current directory")
        
        if 'get content[null]' in line:
            print(f"  ↳ Getting null content")
    
    def handle_get_operation(self, line: str):
        """Handle get operations for fetching data"""
        print(f"✓ Get operation")
        
        # Handle table[content] access
        if 'table[content]' in line:
            print(f"  ↳ Accessing table content")
        
        # Handle file operations
        if 'file' in line and 'file_ext' in line:
            print(f"  ↳ File retrieval operation")
        
        # Handle content[null]
        if 'content[null]' in line:
            print(f"  ↳ Accessing null content")
        
        # Handle glob patterns
        if '-glob' in line:
            print(f"  ↳ Using glob pattern")
    
    def handle_in_operation(self, line: str):
        """Handle in operations for context/scope"""
        print(f"✓ In operation")
        
        # Handle env[activate] access
        if 'env[activate]' in line:
            print(f"  ↳ Environment activation context")
            if self.active_environment:
                print(f"  ↳ Active environment: {self.active_environment}")
        
        # Handle env[content]
        if 'env[content]' in line:
            print(f"  ↳ Environment content context")
        
        # Handle file is STR
        if 'file is STR' in line:
            print(f"  ↳ File as string context")
        
        # Handle -glob default
        if '-glob default' in line:
            print(f"  ↳ Default glob pattern")
        
        # Handle this.* references
        if 'this.' in line:
            this_ref = re.search(r'this\.(\w+)', line)
            if this_ref:
                print(f"  ↳ This reference: {this_ref.group(1)}")
    
    def handle_devrc_command(self, tokens: List[str]):
        """Handle .devrc specific commands"""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token == '-out' and i + 1 < len(tokens):
                self.output_to_file(tokens[i + 1])
                i += 2
            
            elif token == '-crfolder' and i + 1 < len(tokens):
                self.create_folder(tokens[i + 1])
                i += 2
            
            elif token == '-pop':
                if i + 1 < len(tokens):
                    print(f"✓ Pop operation: {tokens[i + 1]}")
                i += 2
            
            elif token == '-plugin':
                print("✓ Plugin mode enabled")
                i += 1
            
            elif token == '-config':
                print("✓ Config mode enabled")
                i += 1
            
            elif token == '-c':
                print("✓ Compile mode enabled")
                i += 1
            
            elif token == '-timed':
                print("✓ Timed operation enabled")
                i += 1
            
            elif token == '-mode' and i + 1 < len(tokens):
                print(f"✓ Mode set to: {tokens[i + 1]}")
                i += 2
            
            elif token == '-force':
                print("✓ Force mode enabled")
                i += 1
            
            elif token == '-a':
                print("✓ Append operation")
                i += 1
            
            elif token == '-locate' and i + 1 < len(tokens):
                print(f"✓ Locate: {tokens[i + 1]}")
                i += 2
            
            elif token == '-to':
                print("✓ Transform operation")
                i += 1
            
            elif token == '-ext' and i + 1 < len(tokens):
                print(f"✓ Extension: {tokens[i + 1]}")
                i += 2
            
            elif token == '-cmdbin':
                print("✓ Command binary mode")
                i += 1
            
            elif token == '-cmdline':
                print("✓ Command line mode")
                i += 1
            
            elif token == '-rline' and i + 1 < len(tokens):
                print(f"✓ Run line: {tokens[i + 1]}")
                i += 2
            
            elif token == '-r' and i + 1 < len(tokens):
                print(f"✓ Run mode: {tokens[i + 1]}")
                i += 2
            
            elif token == '-byp':
                print("✓ Bypass mode enabled")
                i += 1
            
            elif token == '-h' and i + 1 < len(tokens):
                print(f"✓ Handle pattern: {tokens[i + 1]}")
                i += 2
            
            elif token == '-ch':
                print("✓ Chain operation")
                i += 1
            
            elif token == '-numline':
                print("✓ Number line mode")
                i += 1
            
            elif token == '-ff':
                print("✓ Fast forward mode")
                i += 1
            
            else:
                i += 1
    
    def handle_if_statement(self, line: str):
        """Handle if statements"""
        # Extract condition
        match = re.search(r'if \((.*?)\) is (.*?)(?:\s+do\s+|\s+|$)', line)
        if match:
            var_name = match.group(1).strip()
            expected = match.group(2).strip()
            
            var_value = self.variables.get(var_name, False)
            expected_value = self.evaluate_expression(expected)
            
            if var_value == expected_value:
                # Execute the rest of the line
                rest = line[match.end():].strip()
                if rest:
                    print(f"✓ Condition met: {var_name} is {expected_value}")
                    self.process_line(rest)
            else:
                print(f"✗ Condition not met: {var_name} is not {expected_value}")
    
    def handle_for_loop(self, line: str):
        """Handle for loops"""
        match = re.search(r'for \((.*?)\)', line)
        if match:
            var_name = match.group(1).strip()
            print(f"✓ For loop over: {var_name}")
            # Execute the rest of the line
            rest = line[match.end():].strip()
            if rest:
                self.process_line(rest)
    
    def handle_do_statement(self, tokens: List[str]):
        """Handle do statements"""
        print(f"✓ Do statement: {' '.join(tokens)}")
        self.handle_devrc_command(tokens)
    
    def execute_section(self, section_name: str):
        """Execute a specific section"""
        if section_name not in self.sections:
            print(f"✗ Section not found: {section_name}")
            return
        
        section_type = self.section_types.get(section_name, "untyped")
        print(f"\n=== Executing section: {section_name} @[{section_type}] ===")
        for line in self.sections[section_name]:
            self.process_line(line)
    
    def execute_all(self):
        """Execute all sections in order"""
        for section_name, lines in self.sections.items():
            self.execute_section(section_name)
    
    def run(self, filepath: str, sections: Optional[List[str]] = None):
        """Run the DevRC interpreter"""
        print(f"DevRC Interpreter - Loading {filepath}")
        print(f"Root directory: {self.root_dir}")
        
        self.sections = self.parse_file(filepath)
        
        print(f"\n✓ Total sections loaded: {len(self.sections)}")
        print(f"✓ Total imports processed: {len(self.imported_files)}")
        if self.active_environment:
            print(f"✓ Active environment: {self.active_environment}")
        
        if sections:
            for section in sections:
                self.execute_section(section)
        else:
            self.execute_all()
        
        print("\n=== Execution complete ===")
        if self.imported_files:
            print(f"Imported files:")
            for imp in self.imported_files:
                print(f"  - {imp}")
        
        if self.environments:
            print(f"\nEnvironments:")
            for env_name, env_info in self.environments.items():
                active = " (active)" if env_name == self.active_environment else ""
                print(f"  - {env_name}{active}")
                print(f"    Path: {env_info['path']}")
        
        # Return to root directory after execution
        if self.active_environment:
            os.chdir(self.root_dir)
            print(f"\n✓ Returned to root directory: {self.root_dir}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='DevRC DSL Interpreter')
    parser.add_argument('file', help='.devrc file to execute')
    parser.add_argument('--section', '-s', action='append', 
                       help='Specific section(s) to execute')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='Parse without executing')
    parser.add_argument('--root', '-r', 
                       help='Set root directory for environments (default: current directory)')
    parser.add_argument('--list-envs', action='store_true',
                       help='List all available environments')
    
    args = parser.parse_args()
    
    interpreter = DevRCInterpreter()
    
    # Set custom root if provided
    if args.root:
        interpreter.root_dir = os.path.abspath(args.root)
        print(f"Root directory set to: {interpreter.root_dir}")
    
    if args.dry_run:
        sections = interpreter.parse_file(args.file)
        print("Parsed sections:")
        for name, lines in sections.items():
            section_type = interpreter.section_types.get(name, "untyped")
            print(f"\n@[{section_type}]")
            print(f"[{name}]")
            for line in lines:
                print(f"  {line}")
        
        if interpreter.environments:
            print("\n\nEnvironments found:")
            for env_name, env_info in interpreter.environments.items():
                print(f"  - {env_name}: {env_info['path']}")
    
    elif args.list_envs:
        # Scan for environment directories in root
        print(f"Scanning for environments in: {interpreter.root_dir}")
        if os.path.exists(interpreter.root_dir):
            for item in os.listdir(interpreter.root_dir):
                item_path = os.path.join(interpreter.root_dir, item)
                if os.path.isdir(item_path):
                    print(f"  - {item}")
    
    else:
        interpreter.run(args.file, args.section)


if __name__ == '__main__':
    main()
