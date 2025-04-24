from datetime import datetime, timedelta
import re
from typing import Dict, List, Optional
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

class User: #classes for loging in
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Member: #class with information about the members
    def __init__(self, member_id: str, first_name: str, last_name: str,
                 contact: str, membership_type: str, date: str):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.membership_type = membership_type
        self.date = date
    
    def get_full_name(self) -> str: #combines first and last name to give someone's full name
        return f"{self.first_name} {self.last_name}"

class Session: #class for the session give you the name of the session like spin class cost and time if it in the day or night
    def __init__(self, session_id: str, name: str, cost: int, schedule: str):
        self.session_id = session_id
        self.name = name
        self.cost = cost
        self.schedule = schedule

class CheckIn: #information you would need when you check in at the front desk
    def __init__(self, member_id: str, timestamp: datetime):
        self.member_id = member_id
        self.timestamp = timestamp
        self.sessions = []
    
    def add_session(self, session_id: str):
        self.sessions.append(session_id)

class Instructor: #information on the person teaching the session
    def __init__(self, instructor_id: str, first_name: str, last_name: str):
        self.instructor_id = instructor_id
        self.first_name = first_name
        self.last_name = last_name
        self.sessions = []
    
    def get_full_name(self) -> str:# combines first and last name to make full name
        return f"{self.first_name} {self.last_name}"

class MembershipPlan:
    def __init__(self, cost: int, included_sessions: int, discount: float):
        self.cost = cost
        self.included_sessions = included_sessions
        self.discount = discount

class GymOnTheRock:
    def __init__(self):
        self.users = {}  # username -> User object
        self.members = {}  # member_id -> Member object
        self.sessions = {}  # session_id -> Session object
        self.check_ins = []  # List of CheckIn objects
        self.instructors = []  # List of Instructor objects
        self.login_attempts = {}  # username -> {attempts, lockout_time}
        self.current_user = None
        self.membership_plans = {  #give you the benefits you get from the different plans you might sign up to
            "Platinum": MembershipPlan(10000, 4, 0.15),
            "Diamond": MembershipPlan(7500, 2, 0.10),
            "Gold": MembershipPlan(4000, 1, 0.05),
            "Standard": MembershipPlan(2000, 0, 0)
        }
        
        # Initialize with some sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        # Add a sample user
        self.users["username"] = User("username", "username123")
        
        # Add sample sessions
        self.sessions["S01"] = Session("S01", "MA Classes", 1100, "Evening")
        self.sessions["S02"] = Session("S02", "Spin Classes", 900, "Morning")
    
    def signup(self) -> bool:
        print("\n [+]Welcome to Gym-On-The-Rock Sign Up ")
        username = input("[+]Please enter a username: ").strip()
        
        if username in self.users:
            print("[+]Error 409: username already has already been stored")
            return False
        
        password = input("[+]Enter a unique password: ").strip()
        
        # Password rules
        if len(password) < 6: #user must enter password with more than six characters
            print("[+]Error 1001: password is too short must be more than six characters")
            return False
        if not re.search(r"[A-Z]", password):# uses the regular expression module to make user has at least oen capital letter
            print("[+]Error 1002: pass must contain one uppercase")
            return False
        if not re.search(r"[a-z]", password):# ensure it has at least one common letter
            print("[+]Error 1003: pass must contain at least one lowercase")
            return False
        if not re.search(r"\d", password): # unsure it has at least one digit
            print("[+]Error 1004: pass must contain one digit")
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): #ensure it has at lease one special character
            print("[+]Error 1005: pass must contain one special char")
            return False
        
        # Add new user
        self.users[username] = User(username, password)
        print("[+]Great, let's start your fitness journey")
        return True
    
    def login(self) -> bool: #this function allow it that after three attempts it locks you out for five minutes
        max_attempts = 3
        lockout_duration = timedelta(minutes=5)
        
        while True: #promts user for user name and password and store it in variables
            print("[+]Start on your fitness journey, Login")
            username = input("[+]Enter username: ").strip()
            password = input("[+]Enter password: ").strip()
            
            if username not in self.login_attempts: #checks username
                self.login_attempts[username] = {"attempts": 0, "lockout_time": None}
            
            user_data = self.login_attempts[username]
            
            if user_data["lockout_time"]:
                if datetime.now() < user_data["lockout_time"]:
                    remaining_lockout = user_data["lockout_time"] - datetime.now()
                    print(f"Account locked. Try again in {remaining_lockout.seconds // 60} minutes and {remaining_lockout.seconds % 60} seconds.")#shows how much time left in your lock out if you get it wrong
                    continue
                else:
                    # Reset lockout after duration has passed
                    user_data["attempts"] = 0
                    user_data["lockout_time"] = None
            
            # Validate credentials
            if username in self.users and self.users[username].password == password:
                print("[+]login attempt successful")
                # Reset attempt counter on successful login
                user_data["attempts"] = 0
                self.current_user = username
                return True
            else:
                user_data["attempts"] += 1
                attempts_left = max_attempts - user_data["attempts"]
                print(f"[+]Your credentials are invalid, {attempts_left} attempts remaining.")
                
                if user_data["attempts"] >= max_attempts:
                    print("[+]Too many failed attempts. The system will logout.")
                    return False
    
    def generate_member_id(self) -> str:#gives you an id number
        return f"M{len(self.members) + 1:04d}"
    
    def member_checkin(self) -> None:
        print("\n [+]Welcome to mem checkin :) ")
        
        while True:
            mem_id = input("[+]Please enter your five-digit ID: ").strip().upper()#prompts user for id number
            if re.match(r"^M\d{4}$", mem_id):
                break
            print("[+]Error 2020: ID must be 5 characters eg. M0007")
        
        if mem_id not in self.members: #checks for members id
            print("[+]Error 1006: Enter valid member ID")
            return
        
        checkin_time = datetime.now()
        new_checkin = CheckIn(mem_id, checkin_time)
        self.check_ins.append(new_checkin)
        
        print(f"[+]Welcome {self.members[mem_id].first_name}") #welcome message for user
        print("[+]You have the following sessions available: ")
        
        for sid, session in self.sessions.items():
            print(f"{sid} {session.name} - ${session.cost} ({session.schedule})")
        
        while True:
            usr_choice = input("[+]Please enter the session ID (e.g. S01) to be able to register (when finished type F)").strip().upper()
            
            if usr_choice == "F":
                break
                
            if usr_choice in self.sessions:
                new_checkin.add_session(usr_choice)
                print(f"[+]You registered for {self.sessions[usr_choice].name}")
            else:
                print("[+]The session ID is invalid")
    
    def add_member(self): #adds new member
        print("\n[+]Let's add a new member ---")
        mem_id = self.generate_member_id()
        
        # Get first name
        while True:
            first_name = input("[+]Enter your first name: ").strip()#prompts user for first name
            if first_name.isalpha():
                break
            print("[+]Error 1008: invalid name, use alpha char only")
        
        last_name = input("[+]Enter your last name: ").strip() #promts user for last name
        contact = input("[+]Enter your contact/phone number: ") #promts user for phone number
        
        # Asks user for membership type
        while True:
            membership_type = input("[+]Select your membership type (Platinum/Diamond/Gold/Standard) ").strip().title()
            if membership_type in ["Platinum", "Diamond", "Gold", "Standard"]:
                break
            print("Error 1009: please select one valid membership type")
        
        # Shows you the imformation you entered so that you can confirm its accurate
        print("\n[+]Please confirm your details:")
        print(f"[+]First Name: {first_name}")
        print(f"[+]Last Name: {last_name}")
        print(f"[+]Contact: {contact}")
        print(f"[+]Membership Type: {membership_type}")
        
        confirm = input("[+]Verify your info is it correct? (Y/N): ").strip().upper()
        if confirm != "Y":
            print("[+]Addition cancelled")
            return
        
        # Create and store the new member
        new_member = Member(
            mem_id, 
            first_name, 
            last_name, 
            contact, 
            membership_type, 
            datetime.now().strftime("%Y-%m-%d")
        )
        
        self.members[mem_id] = new_member
        print(f"[+]You have successfully added member {mem_id}")
    
    def manage_sessions(self):
        print("\n [+]Session Management")
        print("[+]Following existing sessions:")
        
        for sid, session in self.sessions.items():
            print(f"[+][{sid}] {session.name} (${session.cost})")

        #gives you the option to create new session or update existing on
        user_prompt = input("\n1. Enter 1 to add new \n2. Enter 2 to update existing sessions: ").strip()
        
        if user_prompt == "1":
            # Generate new session ID
            if self.sessions:
                max_num = max(int(sid[1:]) for sid in self.sessions if sid.startswith("S") and sid[1:].isdigit())
                session_id = f"S{max_num + 1:02d}"
            else:
                session_id = "S01"
            
            # Get session details
            name = input("[+]Session Name: ").strip()
            cost = int(input("[+]The cost is: $").strip())
            schedule = input("Schedule = (Morning|Evening|Both): ").strip().title()
            
            # Create and store the new session
            new_session = Session(session_id, name, cost, schedule)
            self.sessions[session_id] = new_session
            print(f"[+]You have successfully added session {session_id}")
            
        elif user_prompt == "2":
            session_id = input("[+]Please enter session ID (e.g,S01): ").strip().upper()
            
            if session_id in self.sessions:
                session = self.sessions[session_id]
                print(f"[+]Your current info: {session.name} - ${session.cost} ({session.schedule})")
                
                # Update session details
                new_cost = int(input("[+]Your new cost is: $").strip())
                new_schedule = input("[+]Your new schedule: ").strip().title()
                
                session.cost = new_cost
                session.schedule = new_schedule
                print("[+]Your session has been updated ")
            else:
                print("Error 1010: Invalid session ID")

    # creates a report with useful information
    def generate_reports(self):
        print("[+]Welcome to Sys reports")
        
        # List all members
        print("\n[+]List of all members and the total num of members:")
        for mid, member in self.members.items():
            print(f"[+]{mid}: {member.first_name} {member.last_name} ({member.membership_type})")
        print(f"\nTotal number of members: {len(self.members)}")
        
        # List all sessions
        print("\n[+]List of all classes and their schedule:")
        for sid, session in self.sessions.items():
            print(f"[+]{sid}: {session.name} - ${session.cost} ({session.schedule})")
        
        # Count members by type and calculate fees
        membership_counts = {"Platinum": 0, "Diamond": 0, "Gold": 0, "Standard": 0}
        membership_fees = {"Platinum": 0, "Diamond": 0, "Gold": 0, "Standard": 0}
        
        for member in self.members.values():
            membership_type = member.membership_type
            membership_counts[membership_type] += 1
            membership_fees[membership_type] += self.membership_plans[membership_type].cost
        
        print("\n[+]List of members for each membership type and total fees:")
        for membership_type, count in membership_counts.items():
            print(f"[+]{membership_type}: {count} members, Total fees: ${membership_fees[membership_type]}")
        
        # Calculate earnings per class
        class_earnings = {sid: 0 for sid in self.sessions}
        print("\n[+]List of members registered for classes && total earnings:")
        
        for checkin in self.check_ins:
            for sid in checkin.sessions:
                if sid in class_earnings:
                    class_earnings[sid] += self.sessions[sid].cost
        
        for sid, earnings in class_earnings.items():
            print(f"[+]{sid}: Total earnings: ${earnings}")
        
        # Calculate total monthly fee per member
        print("\n[+]Report for each client with total monthly fee:")
        
        for mid, member in self.members.items():
            membership_plan = self.membership_plans[member.membership_type]
            membership_cost = membership_plan.cost
            included_sessions = membership_plan.included_sessions
            discount = membership_plan.discount
            
            # Get all sessions for this member
            all_sessions = []
            for checkin in self.check_ins:
                if checkin.member_id == mid:
                    all_sessions.extend(checkin.sessions)
            
            # Calculate additional session costs
            session_cost = 0
            if len(all_sessions) > included_sessions:
                paid_sessions = all_sessions[included_sessions:]
                for sid in paid_sessions:
                    if sid in self.sessions:
                        session_cost += self.sessions[sid].cost * (1 - discount)
            
            member_total = membership_cost + session_cost
            print(f"[+]{mid}: {member.first_name} {member.last_name}, Contact: {member.contact}, "
                  f"Membership Type: {member.membership_type}, Total monthly fee: ${member_total}")
        
        # List available sessions
        print("\n[+]You have the following existing sessions:")
        for sid, session in self.sessions.items():
            print(f"[+][{sid}] {session.name} (${session.cost})")
    
    def add_instructor(self):
        print("\n[+]Add instructor ")
        
        instructors_list = [
            "Jaxon Steele",
            "Blake Titan",
            "Ryder Knox",
            "Logan Vega",
            "Dante Storm",
        ]
        
        print("[+]Available instructors:")
        for i, name in enumerate(instructors_list, 1):
            print(f"{i}. {name}")
        
        # Get instructor choice
        while True:
            try:
                choice = int(input("[+]Select your instructor (1-5): "))
                if 1 <= choice <= 5:
                    break
            except:
                pass
            print("[+]Invalid choice.")
        
        selected = instructors_list[choice - 1]
        first, last = selected.split()
        
        # Generate instructor ID
        instructor_id = f"I{len(self.instructors) + 1:03d}"
        
        # Create and store new instructor
        new_instructor = Instructor(instructor_id, first, last)
        self.instructors.append(new_instructor)
        
        print(f"[+]Instructor {instructor_id} added: {selected}")
    
    def display_main_menu(self):
        # Display current user details if logged in
        if self.current_user and self.current_user in self.users:
            print(f"\nWelcome, {self.current_user}!")
            
            # Find user's sessions and calculate total cost
            user_sessions = []
            total_cost = 0
            
            # Check if the current user is a member
            member_id = None
            for mid, member in self.members.items():
                if member.first_name.lower() == self.current_user.lower():
                    member_id = mid
                    break
            
            if member_id:
                for checkin in self.check_ins:
                    if checkin.member_id == member_id:
                        user_sessions.extend(checkin.sessions)
                
                if user_sessions:
                    print("[+]Registered sessions:")
                    for sid in user_sessions:
                        session = self.sessions.get(sid)
                        if session:
                            print(f"  - {session.name}: ${session.cost}")
                            total_cost += session.cost
                    print(f"[+]Cost of current sessions: ${total_cost}")
                else:
                    print("[+]You are not registered for any sessions.")
        
        # Create and display menu
        menu = ConsoleMenu(
            title="\033[36mGYM-ON-THE-ROCK\033[0m",
            subtitle="\033[32mBorn From The Fire Birthplace of Strength\033[0m",
        )
        
        items = [
            FunctionItem("\033[33mMember Check-in\033[0m", self.member_checkin),
            FunctionItem("\033[32mAdd A Member(s)\033[0m", self.add_member),
            FunctionItem("\033[34mManage Your Sessions\033[0m", self.manage_sessions),
            FunctionItem("\033[35mAdd an Instructor\033[0m", self.add_instructor),
            FunctionItem("\033[36mGenerate Your Reports\033[0m", self.generate_reports),
        ]
        
        for item in items:
            menu.append_item(item)
        
        menu.show()
    
    def run(self):
        try:
            banner = r"""
   _____                        ____           _______ _                 _____            _
  / ____|                      / __ \         |__   __| |               |  __ \          | |
 | |  __ _   _ _ __ ___ ______| |  | |_ __ ______| |  | |__   ___ ______| |__) |___   ___| | __
 | | |_ | | | | '_ ` _ \______| |  | | '_ \______| |  | '_ \ / _ \______|  _  // _ \ / __| |/ /
 | |__| | |_| | | | | | |     | |__| | | | |     | |  | | | |  __/      | | \ \ (_) | (__|   <
  \_____|\__, |_| |_| |_|      \____/|_| |_|     |_|  |_| |_|\___|      |_|  \_\___/ \___|_|\_\\
          __/ |
         |___/
"""
            print(banner)
            print("[+]Welcome to Gym-On-The-Rock, The Birth Place of Strength\n")
            
            while True:
                user_prompt = input("[+]Are you a member? you can become a member by selecting 1. Signing up or 2. Login: ")
                
                if user_prompt == "2" and self.login():
                    self.display_main_menu()
                    break
                elif user_prompt == "1":
                    self.signup()
                else:
                    print("Error 2003: Enter a valid option")
                    
        except KeyboardInterrupt:
            print("\n^C\n[+]Have a nice day:)")
        except Exception as e:
            print(f"[+]An error occurred:(: {e}")
        finally:
            print("[+]Have a nice day:)")

# Main entry point
if __name__ == "__main__":
    gym = GymOnTheRock()
    gym.run()
