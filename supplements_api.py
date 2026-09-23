import tkinter as tk
from tkinter import messagebox
import requests
import urllib3
import threading

# إخفاء تحذيرات الأمان
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_data():
    search_term = search_entry.get().strip()
    
    if not search_term:
        messagebox.showwarning("Warning", "Please enter a brand or company name!")
        return

    result_label.config(text="Searching database... Please wait.", fg="#0056b3", justify="center")
    
    search_query = search_term.replace(" ", "+")
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={search_query}&search_simple=1&action=process&json=1"
    headers = {"User-Agent": "MojtabaBrandApp/1.0 - SIT Project"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('count', 0) > 0:
                # جلب أول 3 منتجات تابعة للشركة أو البراند
                products = data['products'][:3] 
                
                info_text = f"--- Top Results for '{search_term}' ---\n\n"
                
                for i, product in enumerate(products, 1):
                    name = product.get('product_name', 'Unknown Product')
                    brand = product.get('brands', 'Unknown Brand')
                    energy = product.get('nutriments', {}).get('energy-kcal_100g', 'N/A')
                    proteins = product.get('nutriments', {}).get('proteins_100g', 'N/A')
                    
                    info_text += f"{i}. {name}\n    Brand: {brand} | Energy: {energy} kcal | Protein: {proteins}g\n\n"
                
                result_label.config(text=info_text, fg="#333333", justify="left")
            else:
                result_label.config(text="No products found for this brand.", fg="#d9534f", justify="center")
        else:
            result_label.config(text=f"Server Error: {response.status_code}", fg="#d9534f", justify="center")
            
    except requests.exceptions.ConnectionError:
        result_label.config(text="Connection Error! Check your internet.", fg="#d9534f", justify="center")
    except Exception as e:
        result_label.config(text="An unexpected error occurred.", fg="#d9534f", justify="center")

def start_search_thread():
    threading.Thread(target=fetch_data, daemon=True).start()

# ==========================================
# تصميم الواجهة (بدون صور، لركز على البيانات)
# ==========================================

root = tk.Tk()
root.title("Brand Info Tracker")
root.geometry("500x500")
root.configure(bg="#ffffff")

main_frame = tk.Frame(root, bg="#ffffff")
main_frame.pack(expand=True, fill="both", pady=20, padx=20)

title_label = tk.Label(main_frame, text="Search Brand or Company", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#222222")
title_label.pack(pady=(10, 20))

search_entry = tk.Entry(main_frame, font=("Segoe UI", 14), width=30, relief="solid", bd=1)
search_entry.pack(pady=10)

search_btn = tk.Button(main_frame, text="Search Info", font=("Segoe UI", 12, "bold"), bg="#28a745", fg="white", 
                       activebackground="#218838", activeforeground="white", relief="flat", padx=20, pady=5,
                       command=start_search_thread)
search_btn.pack(pady=15)

# مساحة عرض النتائج المتعددة
result_label = tk.Label(main_frame, text="", font=("Segoe UI", 11), bg="#ffffff", justify="left")
result_label.pack(pady=10, fill="x")

root.mainloop()