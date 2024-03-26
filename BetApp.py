import tkinter as tk
import requests

class BettingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Betting App")
        self.geometry("600x650")

        # Set your API key
        self.API_KEY = 'API_KEY '
        # Base URL for OddsAPI
        self.BASE_URL = 'https://api.the-odds-api.com/v4/'

        # Fetch sports data
        self.sports_data = self.fetch_sports_data()

        # Create and layout widgets
        self.label_sports = tk.Label(self, text="Select Sport:")
        self.sports_combobox = tk.Listbox(self, width=30, height=10)
        self.button_get_odds = tk.Button(self, text="Get Odds", command=self.get_odds)
        self.label_odds = tk.Label(self, text="Odds:")
        self.odds_listbox = tk.Listbox(self, width=50, height=15)
        self.label_bet_amount = tk.Label(self, text="Enter Bet Amount:")
        self.entry_bet_amount = tk.Entry(self)
        self.button_place_bet = tk.Button(self, text="Place Bet", command=self.place_bet)

        self.label_sports.pack()
        self.sports_combobox.pack()
        self.button_get_odds.pack()
        self.label_odds.pack()
        self.odds_listbox.pack()
        self.label_bet_amount.pack()
        self.entry_bet_amount.pack()
        self.button_place_bet.pack()

        # Populate sports combobox
        self.populate_sports_combobox()

    def fetch_sports_data(self):
        """
        Fetches sports data using the API key and base URL.
        Returns the JSON response if the status code is 200,
        otherwise prints an error message and returns None. 
        """
        try:
            endpoint = f'sports?apiKey={self.API_KEY}'
            response = requests.get(self.BASE_URL + endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def populate_sports_combobox(self):
        """
        Populates the sports combobox with the titles from the fetched sports data.
        """
        if not self.sports_data:
            print("Failed to fetch sports data.")
            return

        try:
            for sport in self.sports_data:
                self.sports_combobox.insert(tk.END, sport['title'])
        except Exception as e:
            print(f"Error occurred while populating sports combobox: {e}")

    def get_odds(self):
        """
        Check if a sport is selected. Make a request to fetch odds data for the selected sport
        from the Odds API. Clear the odds listbox and display the data in the odds listbox.
        Handle exceptions and display appropriate error messages.
        """
        
        if not self.sports_combobox.curselection():
            print("Please select a sport.")
            return

        try:
            selected_sport = self.sports_combobox.get(tk.ACTIVE).lower()
            endpoint = f'sports/upcoming/odds/?regions=us&markets=h2h&oddsFormat=american&apiKey={self.API_KEY}'
            data = self.make_request(endpoint)

            if data:
                self.odds_listbox.delete(0, tk.END)
                for event in data:
                    home_team = event.get('home_team')
                    away_team = event.get('away_team')
                    if home_team and away_team:
                        bookmakers = event.get('bookmakers', [])
                        for bookmaker in bookmakers:
                            markets = bookmaker.get('markets', [])
                            for market in markets:
                                if market['key'] == 'h2h':
                                    outcomes = market.get('outcomes', [])
                                    for outcome in outcomes:
                                        name = outcome.get('name')
                                        price = outcome.get('price')
                                        if name and price is not None:
                                            self.odds_listbox.insert(tk.END, f"{home_team} vs {away_team}: {name} - {price}")
                    else:
                        self.odds_listbox.insert(tk.END, "No event information available")
            else:
                print("Failed to fetch odds data.")
        except Exception as e:
            print(f"Error occurred while fetching odds data: {e}")
            self.odds_listbox.insert(tk.END, "Error occurred while fetching odds data")

    def make_request(self, endpoint):
        """
        Sends a request to the specified endpoint and returns the JSON response if the status code is 200.
        If the request fails, it prints the status code or the exception message and returns None.
        """
        try:
            response = requests.get(self.BASE_URL + endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
        
    def place_bet(self):
        """
        A method to place a bet based on selected odds and bet amount.
        """
        try:
            # Implement your logic to place a bet based on selected odds and bet amount
            pass
        except Exception as e:
            print(f"Error occurred while placing bet: {e}")

if __name__ == "__main__":
    app = BettingApp()
    app.mainloop()

