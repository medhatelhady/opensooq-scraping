from helper import *









#### UPDATE HERE #############################################################################
                                                                                             #
                                                                                             #
# change user name and password                                                              #
USER_NAME = '962785550771'                                                                   #
PASSWORD = 'Aa@123456789'                                                                      #
                                                                                             #
# pick a city OR LINK                                                                               #
CITY_OR_LINK = 'Amman' #
FILE_NAME = 'AMMAN'
                                                                                             #
# name of file where data will be saved                                                      #
SAVE_AT = 'Amman5'                                                                           #
                                                                                             #
                                                                                             #
##############################################################################################

















# don't touch
url = 'https://jo.opensooq.com/en/login'
BASE_LINK = 'https://jo.opensooq.com'

if __name__ == '__main__':
    driver = open_chrome(url)
    login(driver, USER_NAME, PASSWORD)
    driver = select_city(driver, CITY_OR_LINK)

    
    #with open('subcat2cat.json', 'r') as f:
        #d = json.load(f)
        
    
    
    page = 1
    
    if not os.path.exists('./'+SAVE_AT):
        os.makedirs('./'+SAVE_AT)
    
    while True:
        driver = display_phone_numbers(driver)
        sleep(2)
        
        product_list = get_products(driver)
       
        all_products = []
        for product in product_list:
            all_products.append(get_product_info(product))
            
        df = pd.DataFrame(all_products)
        
        df = get_main_category(df)
        df.to_csv('./'+SAVE_AT+'/'+FILE_NAME+'-{}.csv'.format(page), index=False)
        page += 1
        try:
            next_page(driver)
        except:
            print("end")
            break
            
