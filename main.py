import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n{'='*60}")
    print(f"Spouštěn: {script_name}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print(f"{script_name} dokončen úspěšně")
        else:
            print(f"{script_name} selhal s kódem {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Chyba při spouštění {script_name}: {e}")
        return False

def main():
    # Seznam skriptů k provedení
    scripts = [
        ('fixCSV.py', ['data/Traffic_delays.csv']),
        ('fixCSV.py', ['data/Traffic_events.csv']),
        ('nehodyAnalysis.py', []),
        ('cykloAnalysis.py', []),
        ('delaysAnalysis.py', []),
        ('eventsAnalysis.py', [])
    ]
    
    results = []
    
    # 1. Oprava CSV souborů
    print("\n1. OPRAVA CSV SOUBORŮ")
    print("-" * 60)
    for i, (script, args) in enumerate(scripts[:2], 1):
        success = run_script(script + ' ' + ' '.join(args) if args else script)
        results.append((script + ' ' + ' '.join(args), success))
    
    # 2. Spuštění analýz
    print("\n2. SPUŠTĚNÍ ANALÝZ")
    print("-" * 60)
    for script, args in scripts[2:]:
        success = run_script(script)
        results.append((script, success))
    
    # Výsledné shrnutí
    print("\n" + "=" * 60)
    print("SHRNUTÍ")
    print("=" * 60)
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    for script, success in results:
        status = "Úspěch" if success else "Selhání"
        print(f"{status:12} - {script}")
    
    print(f"\nCelkem: {success_count}/{total_count} úspěšných")
    
    if success_count == total_count:
        print("\nVšechny analýzy byly dokončeny úspěšně!")
        return 0
    else:
        print(f"\n{total_count - success_count} analýz selhalo")
        return 1

if __name__ == '__main__':
    sys.exit(main())
