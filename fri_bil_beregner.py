from dateutil import relativedelta
from datetime import datetime
from datetime import date


# Some typing left out due to untertainty of input datasrouce
# More input validation should be added when input source is validated
def calculate_value(price: int|float ,yearly_periodic_toll: int|float ,registration_date,purchase_date, tax_year: int):
    """
    Calculates the value of a car based on its purchase price, registration date, yearly periodic tax, and tax year.

    Args:
        price (int|float): The purchase price of the car.
        yearly_periodic_tax (int|float): The yearly periodic tax for the car.
        registration_date: The registration date of the car in the format "Month Day Year", e.g., "December 30 2022".
        purchase_date: The purchase date of the car in the format "Month Day Year", e.g., "December 31 2023".
        tax_year (int): The tax year for which to calculate the car value.

    Raises:
            ValueError: If tax_year is less than or equal to 2023.

    Returns:
       int: A tuple containing the calculated total value of the car, the environmental tax, the yearly value, and the monthly value.
    """

    # Check if tax year is valid
    if tax_year < 2023:
        raise ValueError("Tax year must be greater than 2022.")
       
    min_price = 160000
    if price < min_price:
        price = min_price

    # Change this depending on input type
    registration_date = datetime.strptime(registration_date, "%B %d %Y").date()
    purchase_date = datetime.strptime(purchase_date, "%B %d %Y").date()
    
    def get_calculated_month_by_dates(registration_date: date, purchase_date: date) -> int:      
        """
        Calculates the number of months between the registration date and the purchase date.

        Args:
            registration_date (date): The registration date of the car.
            purchase_date (date): The purchase date of the car.

        Returns:
            total_months (int): The number of months between the registration date and the purchase date.
        """
        

        months = relativedelta.relativedelta(purchase_date, registration_date).months
        years = relativedelta.relativedelta(purchase_date, registration_date).years

        total_months = years * 12 + months
        if relativedelta.relativedelta(purchase_date, registration_date).days > 0:
            total_months += 1

        return total_months    

    

    def months_since_reg(registration_date,tax_year: int):
        """
        Calculates the number of months between the registration date and the cutoff date for the given tax year.

        Args:
            registration_date: The registration date of the car.
            tax_year (int): The tax year for which to calculate the number of months.

        Returns:
            The number of months between the registration date and the cutoff date for the given tax year.
        """
        cut_off_date = datetime.strptime(f"december 31 {tax_year - 1}", "%B %d %Y").date()
        
        months = relativedelta.relativedelta(cut_off_date, registration_date).months
        years = relativedelta.relativedelta(cut_off_date, registration_date).years

        total_months = years * 12 + months
        if relativedelta.relativedelta(cut_off_date, registration_date).days > 0:
            total_months += 1

        return total_months   

    def calculate_price(price: int|float):
        """
        Calculate the final price of a car, based on its original price and the dates of registration and purchase.

        Args:
        - price (int|float): the original price of the car.

        Returns:
        - float: the final price of the car, after applying any special discounts or adjustments.

        Special discounts may be applied if the car is bought within 3 years of its first registration date, but the number of months
        between the December prior to the tax year and the first registration year is greater than or equal to 36. In this case, the 
        price is reduced by 25%.
        """
        
        months_in_three_years = 36
        months_between_registration_and_purchase = get_calculated_month_by_dates(registration_date,purchase_date)
        months_since_registration_from_december_before_taxyear = months_since_reg(registration_date,tax_year)

        # When a car is bought within 3 years of first registration date, but months between december prior taxyear and first registration year is >= 36
        # When this specific condition is met, the price is calculated at 75% of purchase price
        if months_between_registration_and_purchase < months_in_three_years and months_since_registration_from_december_before_taxyear >= months_in_three_years:
            price = price * 0.75
        
        return price

    def calculate_car_value(price: int|float, tax_year: int):
        """
        Calculates the taxation value for a car based on its price and the tax year.

        Args:
            price (float): The price of the car in Danish kroner (DKK).
            tax_year (int): The tax year to calculate the taxation value for.

        

        Returns:
            float: The calculated taxation value.
        """

        

        # Fixed value for calculation
        fixed_value = 300000

        # Calculate taxation value based on tax year and price
        if tax_year >= 2025:
            rate = 0.225
        elif tax_year == 2024:
            if price < fixed_value:
                rate = 0.23
            else:
                rate_over_300000 = 0.22
                rate_under_300000 = 0.23
                residual_amount = max(price - fixed_value, 0)
                taxation_value = (residual_amount * rate_over_300000) + (fixed_value * rate_under_300000)
                return taxation_value
        elif tax_year == 2023:
            if price < fixed_value:
                rate = 0.235
            else:
                rate_over_300000 = 0.215
                rate_under_300000 = 0.235
                residual_amount = max(price - fixed_value, 0)
                taxation_value = (residual_amount * rate_over_300000) + (fixed_value * rate_under_300000)
                return taxation_value

        return price * rate


    
    def calculate_environmental_tax(årlig_periodisk_afgift: int |float, year: int):
        """
        Calculates the environmental tax value based on the annual periodic tax and the tax year.

        Args:
        - årlig_periodisk_afgift (float): The annual periodic tax value.
        - year (int): The tax year.

        Returns:
        - environmental_tax_value (float): The calculated environmental tax value.

        """
      

        # Calculate the environmental tax value based on the tax year
        if year >= 2025:
            rate = 7
        elif year == 2024:
            rate = 6
        else:
            rate = 4.5

        environmental_toll_value = årlig_periodisk_afgift * rate
        return environmental_toll_value

        

    def calculate_yearly_value(taxation_value: int|float, environmental_toll_value: int|float):
        """
        Calculate the yearly value of a car, including both taxation and environmental taxes.

        Args:
        - taxation_value (float): The value of the car after taxation.
        - environmental_tax_value (float): The value of the environmental tax.

        Returns:
        - float: The yearly value of the car, including taxation and environmental taxes.

        """
        return taxation_value + environmental_toll_value 

    def calculate_monthly_Value(årlig_værdi: int|float):
        """
        Calculate the monthly value of a car.

        Args:
        - årlig_værdi (float): The yearly value of the car.

        Returns:
        - float: The monthly value of the car.

        """
        return årlig_værdi / 12
    
    
   

    environmental_toll = calculate_environmental_tax(yearly_periodic_toll, tax_year)
    price = calculate_price(price)
    total_value = calculate_car_value(price,tax_year)
    yearly_value = calculate_yearly_value(total_value ,environmental_toll)
    monthly_value = calculate_monthly_Value(yearly_value)
        
        
    return total_value, environmental_toll, yearly_value, monthly_value

   

samlet_værdi, miljø_afgift, årlig_værdi, månedlig_værdi = calculate_value(500000,660,"december 30 2022","december 31 2023" ,2023)


print (samlet_værdi, miljø_afgift, årlig_værdi, månedlig_værdi)