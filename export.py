import pandas as pd

a = pd.read_csv('check 0.csv')
b = pd.read_csv('errors 0.csv')
a = a.set_index(("id_number"))  # Align on 'id'
b = b.set_index(("id_number"))  # Align on 'id'
a.update(b)            # Update matching rows in a with b
a.reset_index(inplace=True)
print(a.head())
a.to_excel('export.xlsx', index=False)