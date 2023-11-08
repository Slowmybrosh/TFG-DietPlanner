from invoke import task, run

@task
def pdf(c):
    """
    Tarea que genera la documentación del proyecto en formato pdf
    """
    print("Generando documentación...")
    run("cd doc && pdflatex -interaction=nonstopmode proyecto.tex && biber proyecto && pdflatex -interaction=nonstopmode proyecto.tex && pdflatex -interaction=nonstopmode proyecto.tex", shell="/bin/sh")

@task
def clean(c):
    """
    Tarea para limpiar los archivos intermedios generados por latex
    """
    print("Limpiando archivos...")
    run("rm -f doc/*.aux doc/*.bbl doc/*.bcf doc/*.blg doc/*.log doc/*.out doc/*.run.xml doc/*.toc", shell="/bin/sh")

@task
def install(c, dev=False):
	"""
	Tarea encargada de instalar las dependencias del programa.

	Si se usa con la flasg --dev se instalarán las dependencias de desarrollo también. 
	"""

	if(dev):
		print("Instalando dependencias de dev...")
		
		run("poetry install", shell="/bin/sh")
	else:
		print("Instalando dependencias...")
		run("poetry install --no-dev", shell="/bin/sh")
            
@task
def installSpell(c):
      print("Instalando dependencias...")
      run("./scripts/spell_install.sh", shell="/bin/sh")

@task
def orderDic(c):
      print("Ordenando diccionario de palabras clave...")
      run("python3 ./scripts/order_dico.py")

@task
def spell(c):
    print("Lanzando script de comprobación...")
    run("./scripts/spell_check.sh",shell="/bin/sh")
    
@task
def workflowSpell(c):
    installSpell(c)
    orderDic(c)
    spell(c)

@task
def migrate(c, app="app"):
    print("migrating data...")
    run(f"poetry run python3 dietplanner/manage.py makemigrations {app}")
    run(f"poetry run python3 dietplanner/manage.py migrate {app}")
@task
def loadData(c):
    print("Cargando datos...")
    run("poetry run python3 dietplanner/manage.py shell < data/load_data.py")

@task
def runserver(c):
    run("poetry run python3 dietplanner/manage.py runserver")

@task
def test(c, test="app.tests.tests"):
    run(f"poetry run dietplanner/manage.py test {test}")