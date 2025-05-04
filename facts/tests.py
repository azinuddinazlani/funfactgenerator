from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .models import FunFact

# Model Tests
class FunFactModelTests(TestCase):
    def test_funfact_creation(self):
        fact = FunFact.objects.create(
            content="Test fact content",
            category="Test"
        )
        self.assertEqual(fact.content, "Test fact content")
        self.assertEqual(fact.category, "Test")
        self.assertEqual(str(fact), "Test fact content")  # Test __str__ method

    def test_funfact_retrieval(self):
        FunFact.objects.create(content="Fact 1", category="Cat1")
        FunFact.objects.create(content="Fact 2", category="Cat2")
        
        facts = FunFact.objects.all()
        self.assertEqual(facts.count(), 2)
        
        cat1_facts = FunFact.objects.filter(category="Cat1")
        self.assertEqual(cat1_facts.count(), 1)
        self.assertEqual(cat1_facts[0].content, "Fact 1")

# View Tests
class ViewTests(TestCase):
    def test_home_view(self):
        # Test home view with no facts
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Test home view with facts
        FunFact.objects.create(content="Test fact", category="Test")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test fact")

    def test_random_fact_api(self):
        # Test API with no facts
        response = self.client.get(reverse('random_fact'))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)
        
        # Test API with facts
        fact = FunFact.objects.create(content="API test fact", category="API")
        response = self.client.get(reverse('random_fact'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['content'], "API test fact")
        self.assertEqual(data['category'], "API")

# Functional Tests
class FunctionalTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(service=service, options=options)
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def setUp(self):
        # Create some test facts
        self.fact1 = FunFact.objects.create(
            content="Functional test fact 1",
            category="Test"
        )
        self.fact2 = FunFact.objects.create(
            content="Functional test fact 2",
            category="Test"
        )
    
    def test_get_new_fact(self):
        # Open the homepage
        self.selenium.get(f"{self.live_server_url}{reverse('home')}")
        
        # Verify the page title
        self.assertIn("Fun Fact Generator", self.selenium.title)
        
        # Get the initial fact
        initial_fact = self.selenium.find_element(By.ID, "fact-content").text
        
        # Click the "Get New Fact" button
        self.selenium.find_element(By.ID, "new-fact-btn").click()
        
        # Wait for the AJAX request to complete
        time.sleep(1)
        
        # Get the new fact
        new_fact = self.selenium.find_element(By.ID, "fact-content").text
        
        # Verify that we got a fact (might be the same due to randomness)
        self.assertTrue(new_fact)
        
        # Click again to make sure we can get multiple facts
        self.selenium.find_element(By.ID, "new-fact-btn").click()
        time.sleep(1)
        another_fact = self.selenium.find_element(By.ID, "fact-content").text
        self.assertTrue(another_fact)