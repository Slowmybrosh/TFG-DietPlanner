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