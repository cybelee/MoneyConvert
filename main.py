import customtkinter as ctk
from src.api_client import FrankfurterAPI
from src.currency_list import get_currencies
from src.searchable_dropdown import SearchableDropdown  

api = FrankfurterAPI()
currency = get_currencies()

currency_options = [
    f'{item["code"]} - {item["name"]}'
     for item in currency
]

print(currency_options)
ctk.set_appearance_mode("light")

BG = "#F4F5F5"
CARD = "#FFFFFF"
DARK = "#040406"
TEAL = "#006262"
MUTED = "#696B70"

app = ctk.CTk(fg_color=BG)
app.title("MoneyConvert")
app.iconbitmap("assets/logoTeam.ico")

app.geometry("420x760")
app.resizable(False, False)
app.attributes("-fullscreen", False) 
header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(fill="x", padx=26, pady=(30, 24))

ctk.CTkLabel(
    header,
    text="MoneyConvert",
    font=("Inter", 25, "bold"),
    text_color=DARK
).pack(anchor="w")

ctk.CTkLabel(
    header,
    text="Kelompok Orang Have",
    font=("Inter", 13),
    text_color=MUTED
).pack(anchor="w", pady=(5, 0))
card = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=24,
    border_width=1,
    border_color="#E5E7E7"
)
card.pack(fill="x", padx=20, pady=5)






def format_amount(event=None):
    value = amount_entry.get()

    digits = "".join(char for char in value if char.isdigit())

    if not digits:
        amount_entry.delete(0, "end")
        return

    formatted = f"{int(digits):,}".replace(",", ".")

    amount_entry.delete(0, "end")
    amount_entry.insert(0, formatted)
    amount_entry.icursor("end")



def get_amount():
    try:
        amount = float(amount_entry.get().replace(".", ""))

        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        base = base_currency.get().split(" - ")[0]
        quote = quote_currency.get().split(" - ")[0]

        result_label.configure(text="Processing...")
        rate_label.configure(text="Fetching exchange rate...")

        result_label.update_idletasks()
        rate_label.update_idletasks()
        rate = api.get_rate(base, quote)
        result = amount * rate

        result_label.configure(
            text=f"{result:,.2f}"
        )

        rate_label.configure(
            text=f"1 {base} = {rate:,.2f} {quote}"
        )

    except ValueError:
        result_label.configure(text="Invalid input")
        rate_label.configure(text="Enter an amount greater than 0")

    except Exception as error:
        result_label.configure(text="Failed to fetch exchange rate")
        rate_label.configure(text=str(error))
ctk.CTkLabel(
    card,
    text="YOU SEND",
    font=("Inter", 11, "bold"),
    text_color=MUTED
).pack(anchor="w", padx=22, pady=(22, 8))

amount_entry = ctk.CTkEntry(
    card,
    height=55,
    placeholder_text="Enter amount",
    font=("Inter", 23),
    fg_color="#F7F8F8",
    text_color=DARK,
    border_width=0,
    corner_radius=12
)
amount_entry.pack(fill="x", padx=20)
amount_entry.bind("<KeyRelease>", format_amount)
base_currency = SearchableDropdown(
    card,
    values=currency_options,
    height=42,
    visible_items=5,
    font=("Inter", 14),
    fg_color="#E9F2F1",
    button_color="#E9F2F1",
    button_hover_color="#D8E8E6",
    text_color=TEAL,
    dropdown_text_color=DARK,
)

base_currency.set(currency_options[1])
base_currency.pack(fill="x", padx=20, pady=(12, 18))

ctk.CTkFrame(
    card,
    height=1,
    fg_color="#E8EAEA"
).pack(fill="x", padx=20)


ctk.CTkLabel(
    card,
    text="YOU RECEIVE",
    font=("Inter", 11, "bold"),
    text_color=MUTED
).pack(anchor="w", padx=22, pady=(18, 8))

quote_currency = SearchableDropdown(
    card,
    values=currency_options,
    height=42,
    visible_items=5,
    font=("Inter", 14),
    fg_color="#E9F2F1",
    button_color="#E9F2F1",
    button_hover_color="#D8E8E6",
    text_color=TEAL,
    dropdown_text_color=DARK
)

quote_currency.set(currency_options[1])
quote_currency.pack(fill="x", padx=20, pady=(12, 18))


result_label = ctk.CTkLabel(
    card,
    text="0.00",
    font=("Inter", 30, "bold"),
    text_color=DARK
)
result_label.pack(anchor="w", padx=22, pady=(16, 0))

rate_label = ctk.CTkLabel(
    card,
    text="Exchange rate will appear here",
    font=("Inter", 11),
    text_color=MUTED
)
rate_label.pack(anchor="w", padx=22, pady=(5, 22))
convert_button = ctk.CTkButton(
    app,
    text="Convert currency  →",
    height=54,
    corner_radius=15,
    fg_color=TEAL,
    hover_color="#214648",
    text_color="#FFFFFF",
    font=("Inter", 15, "bold"),
    command=get_amount
)
convert_button.pack(fill="x", padx=20, pady=22)
ctk.CTkLabel(
    app,
    text="Rates powered by Frankfurter API",
    font=("Inter", 11),
    text_color=MUTED
).pack(pady=(4, 10))


app.mainloop()
