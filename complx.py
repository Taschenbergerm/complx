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
    
    
    Type in `help` to  get started 
    You can exit  with `exit`
    """
    prompt = "cplx> "

    def __init__(self, *args, **kwargs):
        super(ComplexLineInterface, self).__init__(self, *args, **kwargs)
        self.home = Path(os.environ.get("COMPLX_HOME"))
        self.db_path = self.home / "cplx.db"

    # General Utility
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

    # the panic button
    def do_panic(self, args):
        pass


    # Setup and interacting with sqlite
    def do_exit(self, args):
        print("Thanks you for using the ComplexLineInterface powerd by Data Solutions")
        return True

    def do_set(self, args):
        """
        set [key]  [value]

        Set keys and values in the database
        currently supported keys are :
        =====================================
        user            :  user for the database
        password        :  password for the database
        keep_download   :  optinal weather or not download files should be keep or not
        source          :  data vendor only trth is supported currently
        intraday        :  weather to target intraday or eod or both when a chain_ric is supplied
        """

    def do_put(self, args):
        """
        put [identifier] [start_date] [end_date]

        puts a request into the local queue which will be processed one a master is called

        Input:
        ==========
        identifier:     either a feed_id or a chain_ric / ric_list which will automatically be transformed to a feed_id
                        according to the preferences set un intraday.
                    Multiple identifiers can be supplied by surrounding them with single quotes
        start_date:  the date from which day onwards data should be pull  format is 'YYYY-MM-DD' surrounded by quotes
        end_date:

        """
    def do_list(self, args):
        pass

    def do_drop(self, args):
        pass

    # Complex Downloader Interaction
    def do_foster(self, args):
        pass

    def do_emergency(self, args):
        pass

    def do_download(self, args):
        pass

    def do_check(self, args):
        pass

    def do_call(self, args):
        pass




if __name__ == "__main__":
    ComplexLineInterface().cmdloop()
