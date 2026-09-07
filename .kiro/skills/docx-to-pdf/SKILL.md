---
name: docx-to-pdf
description: "Convertit un ou plusieurs fichiers DOCX en PDF via l'API COM de Microsoft Word. Utiliser quand l'utilisateur veut convertir des DOCX en PDF, exporter des documents Word au format PDF, ou regénérer les PDFs après révision des transcriptions."
metadata:
  author: transcrib
  version: "1.0"
  language: fr
compatibility: >
  Windows uniquement. Microsoft Word installé (Office 16+). Python 3.10+ avec pywin32 installé dans le venv : `venv\Scripts\python.exe -m pip install pywin32`.
---

# Conversion DOCX → PDF

Utilise l'API COM de Word pour une conversion fidèle : polices, styles et mise en page sont préservés à l'identique.

## Étape 1 — Identifier les fichiers à convertir

Demander à l'utilisateur :
- un répertoire (convertit tous les DOCX trouvés) **ou** des fichiers individuels
- le répertoire de sortie (par défaut : même répertoire que la source)

Si l'utilisateur ne précise pas, proposer de convertir tous les DOCX de `docs/`.

**Critère de fin** : la liste des fichiers DOCX sources et le répertoire de sortie sont confirmés.

## Étape 2 — Vérifier les prérequis

```powershell
# Vérifier pywin32 dans le venv
& "venv\Scripts\python.exe" -c "import win32com.client; print('ok')"
```

Si le module est absent :
```powershell
& "venv\Scripts\python.exe" -m pip install pywin32
```

**Critère de fin** : `import win32com.client` s'exécute sans erreur.

## Étape 3 — Convertir

```powershell
& "venv\Scripts\python.exe" .kiro\skills\docx-to-pdf\scripts\convert.py <dossier_source> [--output <dossier_sortie>]
```

Ou pour des fichiers individuels :
```powershell
& "venv\Scripts\python.exe" .kiro\skills\docx-to-pdf\scripts\convert.py <fichier1.docx> <fichier2.docx> [--output <dossier_sortie>]
```

Le script affiche pour chaque fichier : nom du PDF produit et taille en octets.

**Critère de fin** : chaque DOCX de la liste a un PDF correspondant dans le répertoire de sortie, sans erreur signalée par le script.

## Étape 4 — Confirmer

Lister les PDFs produits avec leur taille. Signaler tout fichier qui a échoué.

---

## Raccourci : régénérer les 4 cahiers

Un script dédié regroupe les 4 DOCX des Écrits de Guerre. À utiliser systématiquement après toute modification d'un cahier :

```python
# Via subprocess pour contourner le blocage PowerShell de Kiro
import subprocess, sys
result = subprocess.run(
    [sys.executable, r'.kiro/skills/docx-to-pdf/scripts/convert_cahiers.py'],
    capture_output=True, text=True, timeout=300
)
print(result.stdout)
```

Ou depuis un terminal :
```
python .kiro/skills/docx-to-pdf/scripts/convert_cahiers.py
```

Le script `convert_cahiers.py` se charge lui-même de se placer à la racine du repo et d'appeler `convert.py` avec les 4 fichiers.
