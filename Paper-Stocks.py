import yfinance as yf
import time

# Checks What User Wants To Do
action = input("Want to View your Portfolio(type v), purchase stocks(type p), or sell stocks(type s)").lower()

# If User Wants to View Their PortFolio
if action == 'v':
    TSfile = open("Total Stocks", 'r')
    for line in TSfile:
        value = line.split()
        # Finds Total Money Spent on Stocks
        previous_total_money = float(value[1]) * float(value[2])

        # Finds Current Stock Value for Stocks
        current_stock_value = round(yf.Ticker(value[0]).fast_info.last_price, 2)

        # Finds Current Total Money on Stocks
        current_total_money = float(value[1]) * float(current_stock_value)

        # Finds Total Change in Money
        total_money_change = current_total_money - previous_total_money
        if total_money_change > 0:
            result = 'Positive'

        # Give All Information Back To User
        print("--------------------------------------")
        print(value[0] + ': ' + value[1] + ' stocks bought at ' + value[2] +' each. \tTotal: ' + str(previous_total_money))
        print(value[0] + ': ' + 'Current stock worth ' + str(current_stock_value) + ' each. \tTotal: ' + str(current_total_money))
        print("Total Change: " + str(round(total_money_change,2)))
        time.sleep(1)

# If User Wants To Purchase Stocks For Their Portfolio
elif action == 'p':
    # Gets Total Money
    TMfile = open("Total Money", 'r')
    total_money = TMfile.read()
    total_money = float(total_money)

    # Gives Total Money to User, stops if user has no money
    if total_money <= 0:
        time.sleep(1)
        print('You currently have ' + str(total_money) + ' dollars. You cannot purchase any stocks.')
        time.sleep(0.5)
        exit(0)
    else:
        print("You currently have", total_money, "in your account.")

    # Gets The Stock The User Wants to Buy
    stockinput_name = input("Enter Stock Name(Ticker Symbol): ")
    stock_name = yf.Ticker(stockinput_name)

    # Gets amount user wants and price per stock
    stock_amount = int(input("How Many Stocks Do You Want to Purchase: "))
    stock_price = round(stock_name.fast_info.last_price, 2)

    # Gets Total Price
    total_stock_price = stock_price * stock_amount

    # Get Money Left
    total_money = total_money - total_stock_price

    # Saves Total Money Left in TOTAL MONEY FILE
    TMfile = open("Total Money", 'w')
    total_money = round(total_money, 2)
    TMfile.write(str(total_money))

    # Saves Stocks Bought and for what price
    TSfile = open("Total Stocks", 'a')
    TSfile.write(str(stockinput_name) + ' ' + str(stock_amount) + ' ' + str(stock_price) + '\n')

elif action == 's':
    # Gets Stock Information
    TSfile = open("Total Stocks", 'r')
    stock_list = []
    amount_stock_list = []
    price_stock_list = []

    # Puts Information In Different Lists
    for line in TSfile:
        value = line.split()
        stock_list.append(value[0])
        amount_stock_list.append(value[1])
        price_stock_list.append(value[2])
    same_stock_price_list = []
    same_stock_amount_list = []

    # Ask user which stock they are selling
    sell_stock = input("Which stock do you want to sell.\nYou have these stocks: " + str(stock_list) + "\nEnter one of the Ticker Symbols: ")
    count = 0
    times = 0

    # Check if they have multiple stocks of that company
    for i in stock_list:
        times +=1
        if i == sell_stock:
            count +=1
            same_stock_price_list.append(price_stock_list[int(times-1)])
            same_stock_amount_list.append(amount_stock_list[int(times-1)])


    # If they don't have multiple stocks
    if count == 1:
        # Get Stock Sell Info
        amount_sell_stock = int(input("How many stocks do you want to sell? You have " + str(same_stock_amount_list) + ' stocks: '))
        stock_name = yf.Ticker(sell_stock)
        stock_price = round(stock_name.fast_info.last_price, 2)
        total_sell_price = stock_price * amount_sell_stock

        # Get Total Money Info and Update It
        TMfile = open("Total Money", 'r')
        total_money = TMfile.read()
        total_money = round(float(total_money) + float(total_sell_price), 2)
        TMfile = open("Total Money", 'w')
        TMfile.write(str(total_money))

        # Update Total Stocks File
        updated_amount_stocks = int(same_stock_amount_list[0]) - int(amount_sell_stock)
        number = -1
        for i in stock_list:
            number += 1
            if i == sell_stock:
                break
        TSfile = open("Total Stocks", 'r')
        lines = TSfile.readlines()
        TSWfile = open("Total Stocks", 'w')
        lines[number] = str(sell_stock) + ' ' + str(updated_amount_stocks) + ' ' + price_stock_list[number] + '\n'
        TSWfile.writelines(lines)

    # If they do have multiple stocks
    else:
        choose_stock = input('Which ' + sell_stock + ' stock do you wish to sell? They each have pricing accordingly: '+
        str(same_stock_price_list) + '\nEnter one of the prices: ')
        number = 0
        for i in same_stock_price_list:
            if i == choose_stock:
                break
            else:
                number +=1
        print(number)
        amount = 0
        for i in price_stock_list:
            if i == choose_stock:
                break
            else:
                amount +=1
        print(amount)
        price_different_stock = same_stock_price_list.index(str(choose_stock))

        amount_sell_stock = int(input("How many stocks do you want to sell? You have " + str(same_stock_amount_list[price_different_stock]) + ' stocks: '))
        stock_name = yf.Ticker(sell_stock)
        stock_price = round(stock_name.fast_info.last_price, 2)
        total_sell_price = stock_price * amount_sell_stock

        # Get Total Money Info and Update It
        TMfile = open("Total Money", 'r')
        total_money = TMfile.read()
        total_money = round(float(total_money) + float(total_sell_price), 2)
        TMfile = open("Total Money", 'w')
        TMfile.write(str(total_money))

        # Update Total Stocks File
        updated_amount_stocks = int(same_stock_amount_list[number]) - int(amount_sell_stock)
        TSfile = open("Total Stocks", 'r')
        lines = TSfile.readlines()
        TSWfile = open("Total Stocks", 'w')
        lines[amount] = str(sell_stock) + ' ' + str(updated_amount_stocks) + ' ' + price_stock_list[amount] + '\n'
        TSWfile.writelines(lines)