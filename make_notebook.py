# -*- coding: utf-8 -*-
"""
Generador modular de celdas para Proyecto_Final_Quiebra_Taiwan.ipynb.
Permite construir el notebook sección por sección de forma completamente reproducible.
"""
import json
import os

def new_notebook():
    return {
        "cells": [],
        "metadata": {
            "colab": {
                "provenance": [],
                "toc_visible": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

def add_md(nb, text):
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

def add_code(nb, code, outputs=None):
    cell = {
        "cell_type": "code",
        "execution_count": len([c for c in nb["cells"] if c["cell_type"] == "code"]) + 1,
        "metadata": {},
        "outputs": outputs or [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    }
    nb["cells"].append(cell)

def save_notebook(nb, path="Proyecto_Final_Quiebra_Taiwan.ipynb"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Notebook guardado en {path} con {len(nb['cells'])} celdas.")
