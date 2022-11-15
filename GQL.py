# we hebben drie objecten nodig: gql, Client en AIOHTTPTransport
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="https://www.badgecraft.eu/api/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)
query = gql(
    """
  mutation {{
    passwordAuthorize(email:"{0}", password:"{1}") {{
      success,
      token
    }}
  }}
""".format(open("email", "r").read(), open("pass", "r").read()))
result = client.execute(query)
if result["passwordAuthorize"]["success"] == True:
    print("Ingelogd")
    # en nu het token bewaren, want die hebben we nodig!
    token = result["passwordAuthorize"]["token"]
else:
    raise ConnectionError("Login niet gelukt. Verkeerde wachtwoord?")

query = gql("""
query {
  me {
    id,
    badges {
      list {
        name
      }
    }
    organisations {
      list {
        name
      }
    }
    projects {
      list {
        name
      }
    }
    quests {
      list {
        badgeClass {
          name
        }
      }
    }
    displayName
  }
}
""")

transport = AIOHTTPTransport(
    url="https://www.badgecraft.eu/api/graphql",
    headers={"Auth-Token": token})
client = Client(transport=transport, fetch_schema_from_transport=True)

# Execute the query on the transport
result = client.execute(query)


def printMenu():
    print(f"|{'-' * 50}|")
    print(f"| 1. Laat organisaties zien{' ' * 24}|")
    print(f"| 2. Laat projecten zien{' ' * 27}|")
    print(f"| 3. Laat badges zien{' ' * 30}|")
    print(f"| 4. Laat naam zien{' ' * 32}|")
    print(f"| 5. Laat quests zien{' ' * 30}|")
    print(f"| 6. Stop het programma{' ' * 28}|")
    print(f"|{'-' * 50}|")

choosing = True
r = True
while r:
    while choosing:
        printMenu()
        choice = input()
        try:
            choice = int(choice)
        except:
            print("Getal moet een cijfer zijn! Probeer opnieuw.")
        else:
            choosing = False
    if choice == 1:
        if len(result['me']["organisations"]["list"]) != 0:
            print(f"{result['me']['displayName']} zit in de volgende organisaties:")
            for organisatie in result['me']["organisations"]["list"]:
                print(organisatie["name"])
        else:
            print(f"{result['me']['displayName']} zit nog niet in een organisatie.")
        print("Druk op enter om door te gaan!")
        input()
    elif choice == 2:
        if len(result['me']["projects"]["list"]) != 0:
            print(f"{result['me']['displayName']} zit in de volgende projecten:")
            for project in result['me']["projects"]["list"]:
                print(project["name"])
        else:
            print(f"{result['me']['displayName']} zit nog niet in een project.")
        print("Druk op enter om door te gaan!")
        input()
    elif choice == 3:
        if len(result['me']["badges"]["list"]) != 0:
            print(f"{result['me']['displayName']} heeft de volgende badges:")
            for project in result['me']["badges"]["list"]:
                print(project["name"])
        else:
            print(f"{result['me']['displayName']} heeft nog geen badges.")
        print("Druk op enter om door te gaan!")
        input()
    elif choice == 4:
        print(f"Zijn naam is {result['me']['displayName']}.")
        print("Druk op enter om door te gaan!")
        input()
    elif choice == 5:
        if len(result['me']["quests"]["list"]) != 0:
            print(f"{result['me']['displayName']} heeft de volgens quests:")
            for quest in result['me']["quests"]["list"]:
                print(quest["name"])
        else:
            print(f"{result['me']['displayName']} heeft op dit moment geen quests.")
        print("Druk op enter om door te gaan!")
        input()
    elif choice == 6:
        print("Doei!")
        r = False
    choosing = True
