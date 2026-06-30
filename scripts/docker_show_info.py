import sys

def main():
    print("\n================ DOCKER SERVICE CHECK ===================")
    print("Services Defined:")
    print("- postgres     (port: 5432)")
    print("- timescaledb  (port: 5433)")
    print("- neo4j        (ports: 7474, 7687)")
    print("- web          (port: 5000)")
    print("=========================================================\n")
    
    ans = input("Proceed with pulling/building these images? (y/n): ").strip().lower()
    if ans != 'y':
        print("Aborting docker start.")
        sys.exit(1)
    print("Execution approved.")

if __name__ == "__main__":
    main()
