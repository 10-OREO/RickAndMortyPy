import sys
import math

s = dict()

def interpret_from_filename(filename):
    with open(filename, 'r') as file:
        lines = list(file.readlines())
    interpret_from_lines(lines)


def interpret_from_lines(lines):
    linenum = -1
    while linenum < len(lines) - 1:
        linenum += 1
        line = lines[linenum].strip()

        if line.startswith("ShowMeWhatYouGot "):
            definition = line.split("ShowMeWhatYouGot ")[1]
            var, val = definition.split("=")
            var = var.replace(" ", "").replace("\n", "")
            val = val.replace(" ", "").replace("\n", "")
            
            if '+' in val:
                LHS, RHS = val.split('+')
                LHS = LHS.strip()
                RHS = RHS.strip()

                left_val = int(s[LHS]) if LHS in s else int(LHS)
                right_val = int(s[RHS]) if RHS in s else int(RHS)

                s[var] = left_val + right_val
            elif '-' in val:
                LHS, RHS = val.split('-')
                LHS = LHS.strip()
                RHS = RHS.strip()

                left_val = int(s[LHS]) if LHS in s else int(LHS)
                right_val = int(s[RHS]) if RHS in s else int(RHS)

                s[var] = left_val - right_val
            elif '*' in val:
                LHS, RHS = val.split('*')
                LHS = LHS.strip()
                RHS = RHS.strip()

                left_val = int(s[LHS]) if LHS in s else int(LHS)
                right_val = int(s[RHS]) if RHS in s else int(RHS)

                s[var] = left_val * right_val
            elif '/' in val:
                LHS, RHS = val.split('/')
                LHS = LHS.strip()
                RHS = RHS.strip()

                left_val = int(s[LHS]) if LHS in s else int(LHS)
                right_val = int(s[RHS]) if RHS in s else int(RHS)

                s[var] = left_val / right_val
            elif '%' in val:
                terms = val.split('%')
                left = terms[0].strip()
                right = terms[1].strip()

                left_val = int(s[left]) if left in s else int(left)
                right_val = int(s[right]) if right in s else int(right)

                s[var] = left_val % right_val
            else:
                s[var] = int(val) if val.isdigit() else varmap(val, s)

        elif line.startswith("YouGottaGetSchwifty"):
            _, iterator_varname, _, start, _, end = line.split()
            start, end = int(start), int(end)
            endlinenum = None
            for linenum_end, line2_end in enumerate(lines[linenum + 1:], start=linenum + 1):
                if line2_end.strip().startswith("OhYeah"):
                    endlinenum = linenum_end
                    break
            if endlinenum is None:
                print("for loop started without end. silly goose")
                return
            else:
                s[iterator_varname] = start
                for i in range(start, end + 1):
                    interpret_from_lines(lines[linenum + 1:endlinenum])
                    s[iterator_varname] += 1
                linenum = endlinenum

        elif line.startswith("WubbaLubba "):
            condition = line.split("WubbaLubba ", 1)[1].strip() 
            condition_met = True  
            conditions = condition.split('||') 

            for or_condition in conditions:
                and_conditions = or_condition.split('&&') 
                and_result = True 

                for and_condition in and_conditions:
                    and_condition = and_condition.strip()
                    if '==' in and_condition:
                        var_name, value = and_condition.split('==')
                        var_name = var_name.strip()
                        value = int(value.strip())
                        and_result = and_result and (varmap(var_name, s) == value)
                    elif '!=' in and_condition:
                        var_name, value = and_condition.split('!=')
                        var_name = var_name.strip()
                        value = int(value.strip())
                        and_result = and_result and (varmap(var_name, s) != value)
                    elif '<' in and_condition:
                        var_name, value = and_condition.split('<')
                        var_name = var_name.strip()
                        value = int(value.strip())
                        and_result = and_result and (varmap(var_name, s) < value)
                    elif '>' in and_condition:
                        var_name, value = and_condition.split('>')
                        var_name = var_name.strip()
                        value = int(value.strip())
                        and_result = and_result and (varmap(var_name, s) > value)
                    elif '<=' in and_condition:
                        var_name, value = and_condition.split('<=')
                        var_name = var_name.strip()
                        value = int(value.strip())
                        and_result = and_result and (varmap(var_name, s) <= value)
                    elif '>=' in and_condition:
                        var_name, value = and_condition.split('>=')
                        var_name = var_name.strip()
                        value = int(value.strip())
                        and_result = and_result and (varmap(var_name, s) >= value)
                    else:
                        print(f"This operator is not allowed :( sorry: {and_condition}")
                        return

                if and_result:
                    condition_met = True
                    break 
                else:
                    condition_met = False 

            endlinenum = None
            for linenum_end, line2_end in enumerate(lines[linenum + 1:], start=linenum + 1):
                if line2_end.strip().startswith("DubDub"):
                    endlinenum = linenum_end
                    break

            if endlinenum is None:
                print("NO WAY!!! if statement without endif")
                return

            if condition_met:
                interpret_from_lines(lines[linenum + 1:endlinenum])

            linenum = endlinenum

        elif line.startswith("while"):
            _, var_name, operator, value = line.split()
            value = int(value)

            endlinenum = None
            for linenum_end, line2_end in enumerate(lines[linenum + 1:], start=linenum + 1):
                if line2_end.strip().startswith("endwhile"):
                    endlinenum = linenum_end
                    break

            if endlinenum is None:
                print("BRUH...while loop without endwhile")
                return

            while True:
                var_value = int(varmap(var_name, s))  

                if operator == '>':
                    condition_met = var_value > value
                elif operator == '<':
                    condition_met = var_value < value
                elif operator == '==':
                    condition_met = var_value == value
                else:
                    print(f"Unsupported operator: ( :(  {operator}")
                    return

                if not condition_met:
                    break

                interpret_from_lines(lines[linenum + 1:endlinenum])

            linenum = endlinenum

        elif line.startswith("AwGeez("):
            print_text = line.split("AwGeez(", 1)[1].replace(")", "").strip()
            if "\"" in print_text:
                print_text = print_text.replace("\"", "")
                print(print_text)
            else:
                val = varmap(print_text, s)
                print(val)

        elif line.startswith("SchwiftyEscape"):
            try:
                _, gravity, mass, radius = line.split()
                gravity = float(gravity.strip())  
                mass = float(mass.strip())  
                radius = float(radius.strip())  
            except ValueError:
                print("You made and ERROR >:(!!! Invalid values for gravity, mass, or radius.")
                return

            escape_velocity = math.sqrt((2 * gravity * mass) / radius)

            print(f"Schwifty Escape velocity calculated: {escape_velocity:.2f} m/s")

        elif line.startswith("SpaceCruiserEquation "):
            _, initial_mass_var, final_mass_var, exhaust_velocity_var = line.split()
            im = float(initial_mass_var)  
            fm = float(final_mass_var)   
            ev = float(exhaust_velocity_var)   
            
            try:
                delta_v = ev * (math.log(im / fm))
                print(f"Space Cruiser Equation: Change of Velocity = {delta_v}")
            except ZeroDivisionError:
                print("STOP MAKING ERRORS >:[ Final mass cannot be zero")
            except ValueError:
                print("Another ERROR!!!!!! Invalid values for masses in SpaceCruiserEquation")
        
        elif line.startswith("RicksLawOfGravitation "):
            try:
                _, m1_var, m2_var, r_var = line.split()
                m1 = float(m1_var)  
                m2 = float(m2_var)  
                r = float(r_var)   
                
                G = 6.67430e-11  
                force = (G * m1 * m2) / (r ** 2) 
                
                print(f"Ricks Gravitational Force calculated: {force:.2e} N")
            except ValueError:
                print("ERROR ERROR ERROR!!! Invalid values for masses or distance.")

        elif line.startswith("SquanchGravity"):
            try:
                _, mass, radius = line.split()
                mass = float(mass.strip()) 
                radius = float(radius.strip())  
            except ValueError:
                print("More ERRORS!!! Invalid values for mass or radius.")
                return

            gravity = (6.67430e-11 * mass) / (radius ** 2)
            print(f"Schwifty surface gravity calculated: {gravity:.2f} m/s²")

        



def varmap(var_name, state):
    if var_name in state:
        return state[var_name]
    else:
        print("Variable referenced but has not been defined: " + var_name)
        quit()

args = sys.argv
if len(args) < 2:
    print("No filename provided to interpreter")
elif len(args) == 2:
    filename = args[1]
    interpret_from_filename(filename)
else:
    print("Too many arguments inputted into interpreter")