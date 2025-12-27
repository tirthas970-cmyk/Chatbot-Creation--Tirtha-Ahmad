def Imprint():
    print("""What would you like to do today? 
1. Access your documents.
2. Type in a document.
""")
    Choice = input("(1/2)")

    if Choice == "2":
        the_Input = input("Document please:")

        filename = "Userfile.txt"

        try:
            with open(filename, 'w') as file:
                file.write(the_Input)
            print("Document saved successfully!")
        except OSError as e:
            print(f"Error saving document: {e}")

        Imprint()
    elif Choice == "1":
        try:
            with open("Userfile.txt", "r") as file:
                content = file.read()
                print("Document content:")
                print(content)
        except FileNotFoundError:
            print("No document found. Create one first with option 2.")
        Imprint()
