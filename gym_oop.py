from datetime import datetime, timedelta
import re
from typing import Dict, List, Optional
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

class User:
    def __init__(my_object, username: str, password: str):
        my_object.username = username
        my_object.password = password

class Member:
    def __init__(my_object, member_id: str, first_name: str, last_name: str, 
                 contact: str, membership_type: str, date: str):
        my_object.member_id = member_id
        my_object.first_name = first_name
        my_object.last_name = last_name
        my_object.contact = contact
        my_object.membership_type = membership_type
        my_object.date = date
    
    def get_full_name(my_object) -> str:
        return f"{my_object.first_name} {my_object.last_name}"

class Session:
    def __init__(my_object, session_id: str, name: str, cost: int, schedule: str):
        my_object.session_id = session_id
        my_object.name = name
        my_object.cost = cost
        my_object.schedule = schedule

class CheckIn:
    def __init__(my_object, member_id: str, timestamp: datetime):
        my_object.member_id = member_id
        my_object.timestamp = timestamp
        my_object.sessions = []
    
    def add_session(my_object, session_id: str):
        my_object.sessions.append(session_id)

class Instructor:
    def __init__(my_object, instructor_id: str, first_name: str, last_name: str):
        my_object.instructor_id = instructor_id
        my_object.first_name = first_name
        my_object.last_name = last_name
        my_object.sessions = []
    
    def get_full_name(my_object) -> str:
        return f"{my_object.first_name} {my_object.last_name}"

class MembershipPlan:
    def __init__(my_object, cost: int, included_sessions: int, discount: float):
        my_object.cost = cost
        my_object.included_sessions = included_sessions
        my_object.discount = discount

class GymOnTheRock:
    def __init__(my_object):
        my_object.users = {}  # username -> User object
        my_object.members = {}  # member_id -> Member object
        my_object.sessions = {}  # session_id -> Session object
        my_object.check_ins = []  # List of CheckIn objects
        my_object.instructors = []  # List of Instructor objects
        my_object.login_attempts = {}  # username -> {attempts, lockout_time}
        my_object.current_user = None
        my_object.membership_plans = {
            "Platinum": MembershipPlan(10000, 4, 0.15),
            "Diamond": MembershipPlan(7500, 2, 0.10),
            "Gold": MembershipPlan(4000, 1, 0.05),
            "Standard": MembershipPlan(2000, 0, 0)
        }
        
        # Initialize with some sample data
        my_object._initialize_sample_data()
    
    def _initialize_sample_data(my_object):
        # Add a sample user
        my_object.users["username"] = User("username", "username123")
        
        # Add sample sessions
        my_object.sessions["S01"] = Session("S01", "MA Classes", 1100, "Evening")
        my_object.sessions["S02"] = Session("S02", "Spin Classes", 900, "Morning")
    
    def signup(my_object) -> bool:
        print("\n [+]Welcome to Gym-On-The-Rock Sign Up ")
        username = input("[+]Please enter a username: ").strip()
        
        if username in my_object.users:
            print("[+]Error 409: username already has already been stored")
            return False
        
        password = input("[+]Enter a unique password: ").strip()
        
        # Password validation
        if len(password) < 6:
            print("[+]Error 1001: pass is too short")
            return False
        if not re.search(r"[A-Z]", password):
            print("[+]Error 1002: pass must contain one uppercase")
            return False
        if not re.search(r"[a-z]", password):
            print("[+]Error 1003: pass must contain at least one lowercase")
            return False
        if not re.search(r"\d", password):
            print("[+]Error 1004: pass must contain one digit")
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            print("[+]Error 1005: pass must contain one special char")
            return False
        
        # Add new user
        my_object.users[username] = User(username, password)
        print("[+]Great, let's start your fitness journey")
        return True
    
    def login(my_object) -> bool:
        max_attempts = 3
        lockout_duration = timedelta(minutes=5)
        
        while True:
            print("[+]Start on your fitness journey, Login")
            username = input("[+]Enter username: ").strip()
            password = input("[+]Enter password: ").strip()
            
            if username not in my_object.login_attempts:
                my_object.login_attempts[username] = {"attempts": 0, "lockout_time": None}
            
            user_data = my_object.login_attempts[username]
            
            if user_data["lockout_time"]:
                if datetime.now() < user_data["lockout_time"]:
                    remaining_lockout = user_data["lockout_time"] - datetime.now()
                    print(f"Account locked. Try again in {remaining_lockout.seconds // 60} minutes and {remaining_lockout.seconds % 60} seconds.")
                    continue
                else:
                    # Reset lockout after duration has passed
                    user_data["attempts"] = 0
                    user_data["lockout_time"] = None
            
            # Validate credentials
            if username in my_object.users and my_object.users[username].password == password:
                print("[+]login attempt successful")
                # Reset attempt counter on successful login
                user_data["attempts"] = 0
                my_object.current_user = username
                return True
            else:
                user_data["attempts"] += 1
                attempts_left = max_attempts - user_data["attempts"]
                print(f"[+]Your credentials are invalid, {attempts_left} attempts remaining.")
                
                if user_data["attempts"] >= max_attempts:
                    print("[+]Too many failed attempts. The system will logout.")
                    return False
    
    def generate_member_id(my_object) -> str:
        return f"M{len(my_object.members)+1:04d}"
    
    def member_checkin(my_object) -> None:
        print("\n [+]Welcome to mem checkin :) ")
        
        while True:
            mem_id = input("[+]Please enter your five-digit ID: ").strip().upper()
            if re.match(r"^M\d{4}$", mem_id):
                break
            print("[+]Error 2020: ID must be 5 characters eg. M0007")
        
        if mem_id not in my_object.members:
            print("[+]Error 1006: Enter valid member ID")
            return
        
        checkin_time = datetime.now()
        new_checkin = CheckIn(mem_id, checkin_time)
        my_object.check_ins.append(new_checkin)
        
        print(f"[+]Welcome {my_object.members[mem_id].first_name}")
        print("[+]You have the following sessions available: ")
        
        for sid, session in my_object.sessions.items():
            print(f"{sid} {session.name} - ${session.cost} ({session.schedule})")
        
        while True:
            usr_choice = input("[+]Please enter the session ID (e.g. S01) to be able to register (when finished type F)").strip().upper()
            
            if usr_choice == "F":
                break
                
            if usr_choice in my_object.sessions:
                new_checkin.add_session(usr_choice)
                print(f"[+]You registered for {my_object.sessions[usr_choice].name}")
            else:
                print("[+]The session ID is invalid")
    
    def add_member(my_object):
        print("\n[+]Let's add a new member ---")
        mem_id = my_object.generate_member_id()
        
        # Get first name
        while True:
            first_name = input("[+]Enter your first name: ").strip()
            if first_name.isalpha():
                break
            print("[+]Error 1008: invalid name, use alpha char only")
        
        last_name = input("[+]Enter your last name: ").strip()
        contact = input("[+]Enter your contact/phone number: ")
        
        # Get membership type
        while True:
            membership_type = input("[+]Select your membership type (Platinum/Diamond/Gold/Standard) ").strip().title()
            if membership_type in ["Platinum", "Diamond", "Gold", "Standard"]:
                break
            print("Error 1009: please select one valid membership type")
        
        # Confirm details
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
        
        my_object.members[mem_id] = new_member
        print(f"[+]You have successfully added member {mem_id}")
    
    def manage_sessions(my_object):
        print("\n [+]Session Management")
        print("[+]Following existing sessions:")
        
        for sid, session in my_object.sessions.items():
            print(f"[+][{sid}] {session.name} (${session.cost})")
        
        user_prompt = input("\n1. Enter 1 to add new \n2. Enter 2 to update existing sessions: ").strip()
        
        if user_prompt == "1":
            # Generate new session ID
            if my_object.sessions:
                max_num = max(int(sid[1:]) for sid in my_object.sessions if sid.startswith("S") and sid[1:].isdigit())
                session_id = f"S{max_num + 1:02d}"
            else:
                session_id = "S01"
            
            # Get session details
            name = input("[+]Session Name: ").strip()
            cost = int(input("[+]The cost is: $").strip())
            schedule = input("Schedule = (Morning|Evening|Both): ").strip().title()
            
            # Create and store the new session
            new_session = Session(session_id, name, cost, schedule)
            my_object.sessions[session_id] = new_session
            print(f"[+]You have successfully added session {session_id}")
            
        elif user_prompt == "2":
            session_id = input("[+]Please enter session ID (e.g,S01): ").strip().upper()
            
            if session_id in my_object.sessions:
                session = my_object.sessions[session_id]
                print(f"[+]Your current info: {session.name} - ${session.cost} ({session.schedule})")
                
                # Update session details
                new_cost = int(input("[+]Your new cost is: $").strip())
                new_schedule = input("[+]Your new schedule: ").strip().title()
                
                session.cost = new_cost
                session.schedule = new_schedule
                print("[+]Your session has been updated ")
            else:
                print("Error 1010: Invalid session ID")
    
    def generate_reports(my_object):
        print("[+]Welcome to Sys reports")
        
        # List all members
        print("\n[+]List of all members and the total num of members:")
        for mid, member in my_object.members.items():
            print(f"[+]{mid}: {member.first_name} {member.last_name} ({member.membership_type})")
        print(f"\nTotal number of members: {len(my_object.members)}")
        
        # List all sessions
        print("\n[+]List of all classes and their schedule:")
        for sid, session in my_object.sessions.items():
            print(f"[+]{sid}: {session.name} - ${session.cost} ({session.schedule})")
        
        # Count members by type and calculate fees
        membership_counts = {"Platinum": 0, "Diamond": 0, "Gold": 0, "Standard": 0}
        membership_fees = {"Platinum": 0, "Diamond": 0, "Gold": 0, "Standard": 0}
        
        for member in my_object.members.values():
            membership_type = member.membership_type
            membership_counts[membership_type] += 1
            membership_fees[membership_type] += my_object.membership_plans[membership_type].cost
        
        print("\n[+]List of members for each membership type and total fees:")
        for membership_type, count in membership_counts.items():
            print(f"[+]{membership_type}: {count} members, Total fees: ${membership_fees[membership_type]}")
        
        # Calculate earnings per class
        class_earnings = {sid: 0 for sid in my_object.sessions}
        print("\n[+]List of members registered for classes && total earnings:")
        
        for checkin in my_object.check_ins:
            for sid in checkin.sessions:
                if sid in class_earnings:
                    class_earnings[sid] += my_object.sessions[sid].cost
        
        for sid, earnings in class_earnings.items():
            print(f"[+]{sid}: Total earnings: ${earnings}")
        
        # Calculate total monthly fee per member
        print("\n[+]Report for each client with total monthly fee:")
        
        for mid, member in my_object.members.items():
            membership_plan = my_object.membership_plans[member.membership_type]
            membership_cost = membership_plan.cost
            included_sessions = membership_plan.included_sessions
            discount = membership_plan.discount
            
            # Get all sessions for this member
            all_sessions = []
            for checkin in my_object.check_ins:
                if checkin.member_id == mid:
                    all_sessions.extend(checkin.sessions)
            
            # Calculate additional session costs
            session_cost = 0
            if len(all_sessions) > included_sessions:
                paid_sessions = all_sessions[included_sessions:]
                for sid in paid_sessions:
                    if sid in my_object.sessions:
                        session_cost += my_object.sessions[sid].cost * (1 - discount)
            
            member_total = membership_cost + session_cost
            print(f"[+]{mid}: {member.first_name} {member.last_name}, Contact: {member.contact}, "
                  f"Membership Type: {member.membership_type}, Total monthly fee: ${member_total}")
        
        # List available sessions
        print("\n[+]You have the following existing sessions:")
        for sid, session in my_object.sessions.items():
            print(f"[+][{sid}] {session.name} (${session.cost})")
    
    def add_instructor(my_object):
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
        instructor_id = f"I{len(my_object.instructors)+1:03d}"
        
        # Create and store new instructor
        new_instructor = Instructor(instructor_id, first, last)
        my_object.instructors.append(new_instructor)
        
        print(f"[+]Instructor {instructor_id} added: {selected}")
    
    def display_main_menu(my_object):
        # Display current user details if logged in
        if my_object.current_user and my_object.current_user in my_object.users:
            print(f"\nWelcome, {my_object.current_user}!")
            
            # Find user's sessions and calculate total cost
            user_sessions = []
            total_cost = 0
            
            # Check if the current user is a member
            member_id = None
            for mid, member in my_object.members.items():
                if member.first_name.lower() == my_object.current_user.lower():
                    member_id = mid
                    break
            
            if member_id:
                for checkin in my_object.check_ins:
                    if checkin.member_id == member_id:
                        user_sessions.extend(checkin.sessions)
                
                if user_sessions:
                    print("[+]Registered sessions:")
                    for sid in user_sessions:
                        session = my_object.sessions.get(sid)
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
            FunctionItem("\033[33mMember Check-in\033[0m", my_object.member_checkin),
            FunctionItem("\033[32mAdd A Member(s)\033[0m", my_object.add_member),
            FunctionItem("\033[34mManage Your Sessions\033[0m", my_object.manage_sessions),
            FunctionItem("\033[35mAdd an Instructor\033[0m", my_object.add_instructor),
            FunctionItem("\033[36mGenerate Your Reports\033[0m", my_object.generate_reports),
        ]
        
        for item in items:
            menu.append_item(item)
        
        menu.show()
    
    def run(my_object):
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
                
                if user_prompt == "2" and my_object.login():
                    my_object.display_main_menu()
                    break
                elif user_prompt == "1":
                    my_object.signup()
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
