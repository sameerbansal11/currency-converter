#!/usr/bin/env python3
"""
currency-converter
Real-time currency converter with live exchange rates,
conversion history, and multi-currency support.

Author: Sameer Bansal
Reg No: RA2311032010061
College: SRM Institute of Science and Technology
Branch: B.Tech CSE (IoT) | Batch: 2023-2027
"""

import urllib.request
import urllib.error
import json
import os
import datetime

# ── Fallback Rates (if no internet) ──────────────────────
FALLBACK_RATES = {
    "USD": 1.0,
    "INR": 83.50,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.50,
    "CAD": 1.36,
    "AUD": 1.53,
    "CHF": 0.90,
    "CNY": 7.24,
    "SGD": 1.34,
    "AED": 3.67,
    "SAR": 3.75,
    "MYR": 4.72,
    "THB": 35.10,
    "KRW": 1325.0,
    "BRL": 4.97,
    "MXN": 17.15,
    "ZAR": 18.63,
    "HKD": 7.82,
    "NZD": 1.63,
}

CURRENCY_NAMES = {
    "USD": "US Dollar",
    "INR": "Indian Rupee",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "SGD": "Singapore Dollar",
    "AED": "UAE Dirham",
    "SAR": "Saudi Riyal",
    "MYR": "Malaysian Ringgit",
    "THB": "Thai Baht",
    "KRW": "South Korean Won",
    "BRL": "Brazilian Real",
    "MXN": "Mexican Peso",
    "ZAR": "South African Rand",
    "HKD": "Hong Kong Dollar",
    "NZD": "New Zealand Dollar",
}

conversion_history = []
rates = {}
rates_source = "fallback"


# ── Fetch Live Rates ──────────────────────────────────────
def fetch_live_rates():
    """Fetch live exchange rates from free API (no key needed)"""
    global rates, rates_source
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get("result") == "success":
                rates = data["rates"]
                rates_source = "live"
                return True
    except Exception:
        pass

    # Try backup API
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            rates = data["rates"]
            rates_source = "live"
            return True
    except Exception:
        pass

    rates = FALLBACK_RATES
    rates_source = "offline (fallback)"
    return False


# ── Core Conversion ───────────────────────────────────────
def convert(amount, from_currency, to_currency):
    """Convert amount from one currency to another"""
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if from_currency not in rates:
        raise ValueError(f"❌ Currency not supported: {from_currency}")
    if to_currency not in rates:
        raise ValueError(f"❌ Currency not supported: {to_currency}")

    # Convert to USD first, then to target
    amount_in_usd = amount / rates[from_currency]
    result = amount_in_usd * rates[to_currency]
    rate = rates[to_currency] / rates[from_currency]
    return round(result, 4), round(rate, 6)


# ── Display Functions ─────────────────────────────────────
def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 56)
    print("       💱 SAMEER'S CURRENCY CONVERTER")
    print("     SRM IST | CSE IoT | RA2311032010061")
    print("=" * 56)


def display_supported_currencies():
    print("\n📋 SUPPORTED CURRENCIES")
    print("-" * 56)
    items = list(CURRENCY_NAMES.items())
    for i in range(0, len(items), 2):
        code1, name1 = items[i]
        rate1 = rates.get(code1, 0)
        line = f"  {code1:<5} {name1:<22} 1 USD = {rate1:<10.4f}"
        if i + 1 < len(items):
            code2, name2 = items[i + 1]
            rate2 = rates.get(code2, 0)
            line += f"  {code2:<5} {name2:<22} 1 USD = {rate2:.4f}"
        print(line)
    print("-" * 56)


def display_history():
    print("\n📜 CONVERSION HISTORY (Last 10)")
    print("-" * 56)
    if not conversion_history:
        print("  No conversions yet.")
    else:
        for i, entry in enumerate(conversion_history[-10:], 1):
            print(f"  {i:2}. {entry}")
    print("-" * 56)


def display_multi_convert(amount, from_currency):
    """Show conversion to all major currencies at once"""
    print(f"\n🌍 {amount} {from_currency} IN ALL CURRENCIES")
    print("-" * 56)
    targets = ["USD", "INR", "EUR", "GBP", "JPY", "CAD", "AUD", "SGD", "AED", "CHF"]
    for target in targets:
        if target == from_currency:
            continue
        try:
            result, rate = convert(amount, from_currency, target)
            name = CURRENCY_NAMES.get(target, target)
            print(f"  {target:<5} {name:<22} → {result:>12,.4f}")
        except Exception:
            pass
    print("-" * 56)


# ── Menu ──────────────────────────────────────────────────
def display_menu():
    print("""
  OPTIONS:
  [1] Convert currency
  [2] Convert to all currencies
  [3] Show all supported currencies
  [4] Show conversion history
  [5] Refresh live rates
  [6] Quick convert (INR ↔ USD)
  [q] Quit
""")


# ── Quick Convert ─────────────────────────────────────────
def quick_convert():
    print("\n⚡ QUICK CONVERT — INR ↔ USD")
    print("-" * 40)
    try:
        val = input("  Enter amount: ").strip()
        amount = float(val)
        r1, _ = convert(amount, "INR", "USD")
        r2, _ = convert(amount, "USD", "INR")
        print(f"\n  💵 {amount:,.2f} INR = {r1:,.4f} USD")
        print(f"  💵 {amount:,.2f} USD = {r2:,.4f} INR")
    except ValueError as e:
        print(f"  {e}")


# ── Main Converter ────────────────────────────────────────
def do_conversion():
    print("\n💱 CURRENCY CONVERSION")
    print("-" * 40)
    print("  (Type 'list' to see all currency codes)\n")

    try:
        from_input = input("  From currency (e.g. USD): ").strip().upper()
        if from_input == "LIST":
            display_supported_currencies()
            return

        to_input = input("  To currency   (e.g. INR): ").strip().upper()
        amount_input = input("  Amount                  : ").strip()

        amount = float(amount_input)
        if amount <= 0:
            print("  ⚠️  Amount must be positive.")
            return

        result, rate = convert(amount, from_input, to_input)

        from_name = CURRENCY_NAMES.get(from_input, from_input)
        to_name = CURRENCY_NAMES.get(to_input, to_input)

        print(f"\n  ┌{'─' * 44}┐")
        print(f"  │  {amount:>12,.4f} {from_input} ({from_name})")
        print(f"  │            = ")
        print(f"  │  {result:>12,.4f} {to_input} ({to_name})")
        print(f"  │")
        print(f"  │  Rate: 1 {from_input} = {rate:.6f} {to_input}")
        print(f"  │  Source: {rates_source}")
        print(f"  └{'─' * 44}┘")

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {amount:,.2f} {from_input} → {result:,.4f} {to_input} (rate: {rate:.4f})"
        conversion_history.append(entry)

    except ValueError as e:
        if "could not convert" in str(e) or "invalid literal" in str(e):
            print("  ⚠️  Invalid amount. Please enter a number.")
        else:
            print(f"  {e}")


# ── Main Loop ─────────────────────────────────────────────
def main():
    display_banner()

    print("\n⏳ Fetching live exchange rates...")
    success = fetch_live_rates()
    if success:
        print(f"  ✅ Live rates loaded successfully!")
    else:
        print(f"  ⚠️  Could not fetch live rates. Using offline fallback rates.")

    print(f"  📡 Rates source : {rates_source}")
    print(f"  💰 Currencies   : {len(rates)} supported")
    print(
        f"  🕐 Time         : {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}"
    )

    display_menu()

    while True:
        try:
            choice = input("\n  Enter option: ").strip().lower()

            if choice == "q":
                print("\n  👋 Goodbye from Sameer's Currency Converter!")
                break
            elif choice == "1":
                do_conversion()
            elif choice == "2":
                print("\n  From currency (e.g. INR): ", end="")
                fc = input().strip().upper()
                print("  Amount: ", end="")
                try:
                    amt = float(input().strip())
                    display_multi_convert(amt, fc)
                except ValueError:
                    print("  ⚠️  Invalid amount.")
            elif choice == "3":
                display_supported_currencies()
            elif choice == "4":
                display_history()
            elif choice == "5":
                print("\n  ⏳ Refreshing rates...")
                fetch_live_rates()
                print(f"  ✅ Rates updated! Source: {rates_source}")
            elif choice == "6":
                quick_convert()
            elif choice == "menu":
                display_menu()
            else:
                print("  ⚠️  Invalid option. Type 'menu' to see options.")

        except KeyboardInterrupt:
            print("\n\n  👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
