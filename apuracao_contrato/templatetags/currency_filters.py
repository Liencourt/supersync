from django import template

register = template.Library()

@register.filter(name='br_currency')
def br_currency(value):
    """
    Formats a number as Brazilian currency (R$ 1.234,56).
    """
    if value is None or value == '':
        return "R$ 0,00"
    try:
        # Convert to float, handling potential comma decimal separator
        if isinstance(value, str):
            value = value.replace(',', '.')
        
        val = float(value)
        
        # Format the number
        formatted_value = f'R$ {val:,.2f}'
        
        # Swap separators
        formatted_value = formatted_value.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return formatted_value
    except (ValueError, TypeError):
        return value
