import os
import sqlite3
from cmd import Cmd
from pathlib import Path


class ComplexLineInterface(Cmd):
    intro = r"""   
        ______                      __          __    _            ____      __            ____
      / ____/___  ____ ___  ____  / /__  _  __/ /   (_)___  ___  /  _/___  / /____  _____/ __/___ _________
     / /   / __ \/ __ `__ \/ __ \/ / _ \| |/_/ /   / / __ \/ _ \ / // __ \/ __/ _ \/ ___/ /_/ __ `/ ___/ _ \
    / /___/ /_/ / / / / / / /_/ / /  __/>  </ /___/ / / / /  __// // / / / /_/  __/ /  / __/ /_/ / /__/  __/
    \____/\____/_/ /_/ /_/ .___/_/\___/_/|_/_____/_/_/ /_/\___/___/_/ /_/\__/\___/_/  /_/  \__,_/\___/\___/
                        /_/
        
        
        
    Welcome to the ComplexLineInterface 
    A command line interface containing all the utilities for the complex team
    This includes an interface to the current trth-complex-app 
    and a panics button which tells you to calm down and gives advice
    """
    prompt = "cplx> "

    def __init__(self, *args, **kwargs):
        super(ComplexLineInterface, self).__init__(self, *args, **kwargs)
        self.home = Path(os.environ.get("COMPLX_HOME"))
        self.db_path = self.home / "cplx.db"

    def do_initdb(self, arguments):
        """
        initdb

        check if a db already exist or not
        if not creates the default database
        """

        if self.db_path.exists():
            print("Database already exists | nothing to do ")
        else:
            conn = sqlite3.connect(self.db_path.resolve())
            conn.execute("""Create TABLE preferences 
                                (key VARCHAR(50) not NULL 
                                value VARCHAR(50);
                            INSERT into preferences(key, value )
                            VALUES
                                    ('keep_download', 'False'),
                                    ('source', 'trth'),
                                    ('intraday', 'False'),
                                    ('db_user', 'NULL'), 
                                    ('db_password', Null),
                                    ('db_host', NULL);""")


            conn.execute("""CREATE TABLE queue(
                                    feed_id INT NOT NULL,
                                    chain_ric VARCHAR(10),
                                    ric_list VARCHAR(10), 
                                    start_date VARCHAR(10),
                                    end_date VARCHAR(10) 
                                    );""")
            print("Database initiated")

    def __add__(self,s):
        return f"Init of cli {s}"

    def do_version(self, arguments):
        """
        version


        displays current verision
        """
        print("v.0.0.1 | Alpha ")

    def do_exit(self, args):
        "Thanks you for using the ComplexLineInterface powerd by Data Solutions"
        return True


if __name__ == "__main__":
    ComplexLineInterface().cmdloop()