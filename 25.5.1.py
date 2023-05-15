import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('/Users/alexandrkrasnov/chromedriver_111/chromedriver')
   pytest.driver.implicitly_wait(5)
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   yield

   pytest.driver.quit()


def test_login_and_My_pets_content():
   WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))

#Вводим учетные данные, входим в эккаунт и с главной страницы переходим на страницу пользователя
   pytest.driver.find_element(By.ID,'email').send_keys('mr.beckers@bk.ru')
   pytest.driver.find_element(By.ID,'pass').send_keys('589172')
   pytest.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   pytest.driver.find_element(By.XPATH, '//a[contains(text(),"Мои питомцы")]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Beckers"
   time.sleep(2)

#Проверяем, что у питомцев из полученного списка указаны имя, порода, возраст

   My_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   My_pets_images = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')
   pets_names=[]
   pets_types=[]
   pets_ages=[]


   for pet in My_pets:
      pets_names.append(pet.text.split(' ')[0])
      pets_types.append(pet.text.split(' ')[1])
      pets_ages.append(pet.text.split(' ')[2])
   print(f'Имена моих питомцев:',pets_names)
   print(f'Количество моих питомцев:',len(pets_names))
   print(f'Порода моих питомцев:', pets_types)
   print(f'Возраст моих питомцев:', [x[0] for x in pets_ages])

# 1.Проверяем наличие фото
   k=0
   for pet in My_pets_images:
         if pet.get_attribute('src') == '':
            k += 1
            print("Данный питомец не имеет фотографии")
   print(f"Число питомцев без фотографии:", k)

# 2.Получаем перечень всех питомцев
   duplicate_names = set()
   duplicate_types = set()
   duplicate_ages = set()
   pets_names_dupl = set()
   pets_types_dupl = set()
   pets_ages_dupl = set()
   for i in range(len(pets_names)):
      assert pets_names[i] != ''
      print(pets_names[i])

# 3.Получаем перечень пород и возрастов
      assert pets_types[i] != ''
      print(pets_types[i])
      assert pets_ages[i] != ''
      print(pets_ages[i][0])

# 4.Проверка отсутствия повторяющихся имён
      if pets_names[i] in duplicate_names:
         pets_names_dupl.add(pets_names[i])
      else:
         duplicate_names.add(pets_names[i])

# 5.Проверка наличия дублирования питомцев
      if (pets_types[i] in duplicate_types) or  (pets_ages[i][0] in duplicate_ages):
         pets_types_dupl.add(pets_names[i])
         pets_ages_dupl.add(pets_ages[i][0])
      else:
         duplicate_types.add(pets_types[i])
         duplicate_ages.add(pets_ages[i][0])

      if (len(pets_names_dupl)>0) and (len(pets_types_dupl)>0) and (len(pets_ages_dupl)>0):
          print( "Есть повторы", pets_names_dupl, ",раз: ", len(pets_names_dupl))
      else:
          print('Нет повторов')