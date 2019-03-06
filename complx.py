import os
import shlex
import sqlite3
from sqlite3 import connect
from cmd import Cmd
from pathlib import Path
from arrow import get
import jinja2 as j2

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
        self.cur = connect(str(self.db_path)).cursor()

    # General Utility
    def do_initdb(self, arguments):
        """
        initdb

        check if a db already exist or not
        if not creates the default database
        """


        self.cur.execute("""Create  TABLE IF NOT EXISTS  preferences 
                            (key VARCHAR(50) not NULL,
                            value VARCHAR(50));""")

        self.cur.execute("""INSERT into preferences(key, value )
                        VALUES
                                ('keep_download', 'False'),
                                ('source', 'trth'),
                                ('intraday', 'False'),
                                ('db_user', 'NULL'), 
                                ('db_password', Null),
                                ('db_host', NULL),
                                ("trth_user", NULL),
                                ("trth_password", NULL);""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS queue(
                                qid INEGER PRIMARY KEY AUTOINCREMENT , 
                                feed_id INT NOT NULL,
                                chain_ric VARCHAR(10),
                                ric_list VARCHAR(10), 
                                start_date VARCHAR(10),
                                end_date VARCHAR(10) 
                                );""")
        print("Database initiated")

    def do_setup(self, args):
        print("Please answer the question to setup the repl")
        user = input("\nWhat's your database username: ")
        pwd = input("What's your database password: ")
        trth_user = input("\nWhats your Thomson Reuters username: ")
        trth_pwd = input("Please supply the Thomsen Reuters password: ")
        pref_keep = input("\n Should download be removed afterwards [y/n]: ")
        pref_intr = input("If not supplied otherwise - do you want to priorites intraday feeds over end of day [y/n]: ")
        keep = self.translate_ans_to_bool(pref_keep)
        intr = self.translate_ans_to_bool(pref_intr)
        sql = j2.Template("""Insert into preferences (key, value) 
        Values 
        {% for key, val in rows %} 
        ('{{key}}', '{{val}}' ) 
        {%if not loop.last %},{%endif%}
        {% endfor %}; 
        """)
        keys = "db_user db_password trth_user trth_password keep_download intraday".split(" ")
        values = [user, pwd, trth_user, trth_pwd, keep, intr]
        rows = list(zip(keys, values))
        query = sql.render(rows=rows)
        print(keys)
        print(values)
        print(rows)
        print(query)
        self.cur.execute(query)
        print("The database is now ready")

    def translate_ans_to_bool(self,ans: str, default: int=0):
        """
        Translate the Y or no to a boolean

        :param ans: Answer supllied by a user
        :type ans: str
        :return: weather or not the answer was yes
        :rtype: bool
        """
        if ans.lower() == "y" :
            return 1
        elif ans.lower() == "n":
            return 0
        else:
            return default

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
        """
        panic [kind of duty]

        The one and only panic button for the trth-app
        It will guide you through the already existing cases of daily duty failure and request from the complex team

        Input:
        =========
        kind of duty    : {daily, missing_data, dirty_database, helpless} What is the problem related to?
                          Are you on daily duty and something went wrong -> daily
                          Did complex ask to download new or missing data -> missing_data
                          Did complex complain about that there are underlying which are actually options -> dirty_database
                          No idea what's going on -> helpless
        """

        if "daily" == args:
            self.daily_panic()
        elif args == "missing_data":
            self.missing_panic()
        elif args == "dirty_database":
            self.dirty_panic()
        else:
            print(r"""¯\_(ツ)_/¯  
Either you forgot to call this function with an argument or I guess nobody can help you now 
so maybe take a breake and get a taco some problems seem to resolve themself 

 /\_/\
(='_' )
(, (") (")
 
 
 
 or call complex to go through this together  Alex and Tobi are always helpful ... 
             🌮 """)


    def daily_panic(self):
        pass

    def missing_panic(self):
        pass

    def dirty_panic(self):
        pass

    # Setup and interacting with sqlite
    def do_exit(self, args):
        print("Thanks you for using the ComplexLineInterface powered by Data Solutions")
        return True

    def do_set(self, args):
        """
        set [key]  [value]

        Set keys and values in the database
        currently supported keys are :
        =====================================
        db_user         :  user for the database
        db_password     :  password for the database
        trth_user       : user for the Thomson Reuters api
        trth_password   : password for the Thomson Reuters api
        keep_download   :  optinal weather or not download files should be keep or not
        source          :  data vendor only trth is supported currently
        intraday        :  weather to target intraday or eod or both when a chain_ric is supplied
        """

        key, val = shlex.split(args)
        print(f"Update preferences set value = {val} where key = {key}")
        #self.cur.execute(f"Update preferences set key = {val} where key = {key}")


    def do_put(self, argument):
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
        args = shlex.split(argument)

        ident = args[0]
        feed = self.find_corr_feed(ident)

        if len(args) == 1:
            ins = f"({feed}, {get().date()}, {get().date()}"
        elif len(args) == 3:
            ins = f"({feed}, '{args[1]}', '{args[2]}' ) "
        else :
            print("Sorry but you only supplied two arguments - please supply either all or only the identifier ")
            ins = None

        if ins:
            print(f"INSERT INTO queue(feed, start_date, end_date)  VALUES {ins}")
            #self.cur.execute()

    def do_list(self, args):
        """
        list [table]

        displays the content of the table.
        Every value for the keys of the preferences could be overwritten using the `set` command
        Every entrie in the queue could be dropped using `drop`

        For more help use `help set` or  `help drop`


        Input:
        ======
        table   : {'queue' or 'preferences' } Display the content of the tables

        """
        print(f"Select * from {args} ")
        #self.cur.execute(f"Select * from {args} ")
        #print(self.cur.fetchall())

    def do_drop(self, args):
        """
        drop [feed | qid]

        drops a feed or qid from the queue
        """
        print(f"delete from queue where feed = {args} or qid = {args}")


    def do_foster(self, args):
        """
        foster

        This will trigger the foster process of the trth via airflow
        The forster process will basically :
            - looks if something expired and creates the follwoing contract
            - merges in newly created requests
            - creates and assignes new feeds for request that dont have one yet
        Be aware that this might take some time so be patient
        """
        self.trigger_dag("foster")

    def do_emergency(self, args):
        """
        emergency

        This will trigger the emergency dag via airflow
        It will check which data are on the dmp and which are missing ( takes some time)
        and then start the daily process with only this feeds.
        Have a look into the documentation for more information """
        self.trigger_dag("emergency")

    def do_download(self, args):
        """
        download [feed] [start_date] [end_date]

        This will download either the current queue or the specified request depending on the input
        No input -> download the queue
        Dateformat =  YYYY-MM-DD e.g. 2019-01-21

        Input:
        =======

        feed        : The feed_id that should be downloaded
        start_date  : From which day this feed should be downloaded
        end_date    :  Up to which day this feed should be downloaded
        """
        arguments = shlex.split(args)

        if arguments:
            self.download_queue()
        elif len(arguments) < 2:
            print(" Please fill either all or no arguments ")
        elif len(arguments) >= 2:
            self.download_feed(*arguments)

    def download_feed(self, feed: int, start_date: str = "", end_date: str = ""):
        pass

    def find_corr_feed(self, identifier):
        pass

    def do_check(self, args):
        """
        check

        Will check wich data are already uploaded on the dmp and which are not
        but in contrast to emergency this will not trigger any download
        it just tells you which feed are not uploaded yet
        """
        pass

    def do_call(self, args):
        pass

    def trigger_dag(self, dag_id):
        """
        Make an API call to airflow and trigger the respective dag
        :param dag_id: The Dag_id that should be triggered
        :type dag_id: str
        :return: Weather or not the call succeded
        :rtype: str
        """

        pass

    def download_queue(self):
        """
        Download the current queue in the sqlite db

        :return: The result of the download
        :rtype: str
        """
        pass


if __name__ == "__main__":
    ComplexLineInterface().cmdloop()
