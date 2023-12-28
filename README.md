# 🏪 ERP
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#-about-the-project">About The Project</a>
      <ul>
        <li><a href="#-modules">Modules</a></li>
        <li><a href="#home-page">Home Page</a></li>
        <li><a href="#product-page">Product Page</a></li>
        <li><a href="#sales-page">Sales Page</a></li>
      </ul>
    </li>
    <li>
      <a href="#-built-with">Built With</a>
    </li>
    <li>
      <a href="#-getting-started">Getting Started</a>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## 🚀 About The Project
A web based ERP software that has the functionalities to deal with Sales, Purchases, orders and returns. It also includes the functionalities to genereate pdf invoices for them. 

### 📁 Modules
  <ul>
    <li>category</li>
    <li>salesman</li> 
    <li>product</li> 
    <li>customer</li>
    <li>vendor</li>
    <li>sales</li>
    <li>purchase</li>
    <li>sales return</li>
    <li>purchase return</li>
    <li>sales Order</li>
    <li>purchase Order</li>
    <li>Delivery Note</li>
    <li>Quotation</li>
    <li>Payment</li>
    <li>Receipt</li>
  </ul>

<h3>Home Page</h3>
<img src="https://github.com/MhdIr7an/ERP/assets/93046265/26e924f4-6686-457f-8170-a01b81a1ea41" width="800" height="400" />


<h3>Product Page</h3>
<img src="https://github.com/MhdIr7an/ERP/assets/93046265/e49cf25b-6d1f-4c05-8b6a-5157ac05e4f2" width="800" height="400" />

<h3>Sales Page</h3>
<img src="https://github.com/MhdIr7an/ERP/assets/93046265/f9843d32-78e9-4610-9c4b-d50d159270d8" width="800" height="400" />



## 🧰 Built With
<div>
<img alt="Django Icon" width="120" height="90" src="https://cdn.iconscout.com/icon/free/png-256/free-django-13-1175187.png?f=webp&amp;w=256">
<img alt="Jquery Icon" width="120" height="80" src="https://cdn.iconscout.com/icon/free/png-256/free-jquery-8-1175153.png?f=webp&amp;w=256">
<img alt="Javascript Icon" width="100" height="80" src="https://cdn.iconscout.com/icon/free/png-256/free-javascript-2038874-1720087.png?f=webp&amp;w=256">
<img alt="Css Icon" width="100" height="80" src="https://cdn.iconscout.com/icon/free/png-256/free-css-38-226095.png?f=webp&amp;w=256">
<img alt="Html Icon" width="100" height="80" src="https://cdn.iconscout.com/icon/free/png-256/free-html-59-225995.png?f=webp&amp;w=256">
</div>

<!-- GETTING STARTED -->
## 🚪 Getting Started

To get a local copy up and running follow these simple example steps.

1. Clone the repo
   ```sh
   git clone https://github.com/MhdIr7an/ERP.git
   ```
2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
3. Download and install WKHTMLTOPDF(required to generate pdf) to C:\Program Files\ from <a href="https://wkhtmltopdf.org/downloads.html">here</a>
4. create a .env file in the root and add SECRET_KEY(Your django secret key)
5. run server
   ```sh
   pip manage.py runserver
   ```

<p align="right">(<a href="#-erp">back to top</a>)<p>
