# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

import time
import os
import glob


def download_wait(cont, directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True

    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload') or fname.endswith('.part'):
                dl_wait = True

        seconds += 1
    fin = os.listdir(directory)
    fin = len(fin)

    # return bool and seconds
    print('Ini',cont)
    print('Fin: ', fin)
    if cont == fin:
        return False,seconds
    else:
        return True,seconds

"""
    Obtengo el modulo que fue invocado
"""
global cont_

module = GetParams("module")

if module == "countDir":
    path_ = GetParams("path_")
    var_ = GetParams("var_")

    cont = os.listdir(path_)
    cont_ = len(cont)

    if cont_ and var_:
         SetVar(var_,cont_)

if module == "DownloadWait":

    path_ = GetParams("path_")
    time_ = GetParams("time_")
    var_ = GetParams("var_")
    var2_ = GetParams("var2_")
    var3_ = GetParams("var3_")

    if path_ and time_:

        try:
            res_,sec_ = download_wait(cont_,path_, int(time_))

            path_ = os.path.join(path_,'*')
            #print('path!!!',path_)
            list_of_files = glob.glob(path_)
            if len(list_of_files) > 0:
                latest_file = max(list_of_files, key=os.path.getctime)
                latest_file = latest_file.replace('\\', '/')
                print(r'' + latest_file, end="")
            else:
                print("Sin archivos", end="")

            SetVar(var2_,res_)
            SetVar(var_,sec_)
            SetVar(var3_,latest_file if res_ else '')

        except Exception as e:
            PrintException()
            raise (e)






