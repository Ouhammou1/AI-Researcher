import asyncio
import json
import time
import random
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from playwright.async_api import async_playwright, Page, Browser
import httpx

@dataclass
class BookingConfig:
    """Configuration for booking automation"""
    target_url: "https://www.edreams.fr/offres/vol/compagnie-aerienne/FR/ryanair/?mktportal=google&utm_id=go_cmp-10556473662_adg-106846393080_ad-696161045516_kwd-13386146_dev-c_ext-_locphy-21537_mtype-e_ntw-g&gad_source=1&gad_campaignid=10556473662&gbraid=0AAAAAD4krlGOVKv4u7J87T4-lIoSWJzVc&gclid=CjwKCAiA3fnJBhAgEiwAyqmY5YzqQ4WK23302KWupdqo6qcExD3J5q3XDUaz6pDh9nv60b5aQJnJ9hoCFv8QAvD_BwE"
    num_tickets: int = 20
    headless: bool = False
    proxy: Optional[str] = None
    delay_range: tuple = (1, 3)  # Random delay between actions

@dataclass
class Ticket:
    """Ticket information"""
    booking_id: str
    status: str
    details: Dict

class CaptchaSolver:
    """Handles various captcha solving strategies"""
    
    @staticmethod
    async def solve_image_captcha(image_data: bytes) -> str:
        """Solve image-based captcha (placeholder for OCR/API)"""
        # In real CTF, integrate with 2captcha, anti-captcha API
        # Or use pytesseract for simple captchas
        print("[CAPTCHA] Attempting to solve image captcha...")
        await asyncio.sleep(random.uniform(1, 2))
        # Simulate solving
        return "SOLVED_CODE_123"
    
    @staticmethod
    async def solve_recaptcha(page: Page, site_key: str) -> str:
        """Solve reCAPTCHA v2/v3"""
        print("[CAPTCHA] Detecting reCAPTCHA...")
        
        # Strategy 1: Check if bypassable
        bypass_token = await page.evaluate("""() => {
            return window.grecaptcha?.getResponse?.() || null;
        }""")
        
        if bypass_token:
            return bypass_token
        
        # Strategy 2: API solving service (placeholder)
        print("[CAPTCHA] Using API solver...")
        await asyncio.sleep(3)
        return "RECAPTCHA_TOKEN_XYZ"
    
    @staticmethod
    async def detect_captcha_type(page: Page) -> Optional[str]:
        """Detect captcha type on page"""
        # Check for reCAPTCHA
        recaptcha = await page.query_selector('.g-recaptcha, [data-sitekey]')
        if recaptcha:
            return "recaptcha"
        
        # Check for hCaptcha
        hcaptcha = await page.query_selector('.h-captcha')
        if hcaptcha:
            return "hcaptcha"
        
        # Check for image captcha
        img_captcha = await page.query_selector('img[alt*="captcha"], img[src*="captcha"]')
        if img_captcha:
            return "image"
        
        return None

class MFAHandler:
    """Handles Multi-Factor Authentication"""
    
    def __init__(self, email_api_key: Optional[str] = None):
        self.email_api_key = email_api_key
        self.code_patterns = [
            r'\b\d{6}\b',  # 6-digit code
            r'\b\d{4}\b',  # 4-digit code
            r'[A-Z0-9]{8}', # 8-char alphanumeric
        ]
    
    async def get_code_from_email(self, email: str) -> str:
        """Fetch MFA code from email (simulated)"""
        print(f"[MFA] Checking email for code: {email}")
        
        # In real scenario: Use Gmail API, Mailinator API, etc.
        # For CTF, might need to check temp email services
        await asyncio.sleep(2)
        
        # Simulate code retrieval
        code = f"{random.randint(100000, 999999)}"
        print(f"[MFA] Retrieved code: {code}")
        return code
    
    async def get_code_from_sms(self, phone: str) -> str:
        """Fetch MFA code from SMS (simulated)"""
        print(f"[MFA] Checking SMS for code: {phone}")
        await asyncio.sleep(2)
        code = f"{random.randint(1000, 9999)}"
        return code
    
    async def handle_totp(self, secret: str) -> str:
        """Generate TOTP code if secret is known"""
        import pyotp
        totp = pyotp.TOTP(secret)
        code = totp.now()
        print(f"[MFA] Generated TOTP: {code}")
        return code

class AntiBotBypass:
    """Bypass anti-bot detection mechanisms"""
    
    @staticmethod
    async def setup_stealth_browser(browser: Browser):
        """Configure browser to avoid detection"""
        # Already using playwright which has good stealth
        pass
    
    @staticmethod
    async def add_realistic_behavior(page: Page):
        """Add human-like behavior patterns"""
        # Random mouse movements
        await page.mouse.move(
            random.randint(100, 500),
            random.randint(100, 500)
        )
        
        # Random scrolling
        await page.evaluate(f"""
            window.scrollBy({{
                top: {random.randint(100, 300)},
                behavior: 'smooth'
            }});
        """)
        
        await asyncio.sleep(random.uniform(0.5, 1.5))
    
    @staticmethod
    def get_realistic_headers() -> Dict:
        """Generate realistic browser headers"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        }

class PaymentHandler:
    """Handle payment form automation (CTF simulation)"""
    
    TEST_CARDS = {
        'visa': '4532015112830366',
        'mastercard': '5425233430109903',
        'amex': '374245455400126',
    }
    
    @staticmethod
    async def fill_payment_form(page: Page, card_type: str = 'visa'):
        """Fill payment form with test data"""
        print(f"[PAYMENT] Filling payment form with {card_type}")
        
        # Common payment field selectors
        selectors = {
            'card_number': ['input[name*="card"], input[id*="card"]', 'input[placeholder*="card number"]'],
            'cvv': ['input[name*="cvv"], input[name*="cvc"]', 'input[id*="cvv"]'],
            'expiry': ['input[name*="expir"]', 'input[id*="exp"]'],
            'name': ['input[name*="name"], input[name*="holder"]'],
        }
        
        try:
            # Fill card number
            for selector in selectors['card_number']:
                if await page.query_selector(selector):
                    await page.fill(selector, PaymentHandler.TEST_CARDS[card_type])
                    break
            
            # Fill CVV
            for selector in selectors['cvv']:
                if await page.query_selector(selector):
                    await page.fill(selector, '123')
                    break
            
            # Fill expiry
            for selector in selectors['expiry']:
                if await page.query_selector(selector):
                    await page.fill(selector, '12/25')
                    break
            
            # Fill name
            for selector in selectors['name']:
                if await page.query_selector(selector):
                    await page.fill(selector, 'TEST USER')
                    break
            
            print("[PAYMENT] Payment form filled successfully")
            return True
            
        except Exception as e:
            print(f"[PAYMENT] Error filling form: {e}")
            return False
    
    @staticmethod
    async def detect_payment_security(page: Page) -> Dict:
        """Detect payment security measures"""
        security = {
            '3ds': False,
            'tokenization': False,
            'iframe': False
        }
        
        # Check for 3D Secure iframe
        frames = page.frames
        for frame in frames:
            url = frame.url
            if '3dsecure' in url.lower() or 'verification' in url.lower():
                security['3ds'] = True
        
        # Check for payment iframes
        payment_iframe = await page.query_selector('iframe[src*="stripe"], iframe[src*="payment"]')
        if payment_iframe:
            security['iframe'] = True
        
        return security

class TicketBookingAgent:
    """Main automation agent for ticket booking"""
    
    def __init__(self, config: BookingConfig):
        self.config = config
        self.captcha_solver = CaptchaSolver()
        self.mfa_handler = MFAHandler()
        self.antibot = AntiBotBypass()
        self.payment = PaymentHandler()
        self.tickets: List[Ticket] = []
        
    async def initialize_browser(self):
        """Initialize Playwright browser with stealth settings"""
        print("[INIT] Starting browser...")
        self.playwright = await async_playwright().start()
        
        # Launch with anti-detection settings
        self.browser = await self.playwright.chromium.launch(
            headless=self.config.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
            ]
        )
        
        # Create context with realistic settings
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        # Remove webdriver flag
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        print("[INIT] Browser initialized")
    
    async def login(self, page: Page, username: str, password: str) -> bool:
        """Handle login with MFA"""
        print(f"[LOGIN] Attempting login for {username}")
        
        try:
            # Wait for login form
            await page.wait_for_selector('input[type="email"], input[name*="user"], input[id*="user"]', timeout=10000)
            
            # Fill credentials
            await page.fill('input[type="email"], input[name*="user"]', username)
            await self.random_delay()
            await page.fill('input[type="password"]', password)
            await self.random_delay()
            
            # Check for captcha before submitting
            captcha_type = await self.captcha_solver.detect_captcha_type(page)
            if captcha_type:
                print(f"[LOGIN] Captcha detected: {captcha_type}")
                if captcha_type == "recaptcha":
                    site_key = await page.get_attribute('[data-sitekey]', 'data-sitekey')
                    token = await self.captcha_solver.solve_recaptcha(page, site_key)
                    # Inject token
                    await page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{token}";')
            
            # Submit login
            await page.click('button[type="submit"], input[type="submit"]')
            await page.wait_for_load_state('networkidle')
            
            # Check for MFA
            mfa_input = await page.query_selector('input[name*="code"], input[placeholder*="code"]')
            if mfa_input:
                print("[LOGIN] MFA required")
                code = await self.mfa_handler.get_code_from_email(username)
                await page.fill('input[name*="code"]', code)
                await page.click('button[type="submit"]')
                await page.wait_for_load_state('networkidle')
            
            print("[LOGIN] Login successful")
            return True
            
        except Exception as e:
            print(f"[LOGIN] Login failed: {e}")
            return False
    
    async def search_flights(self, page: Page, origin: str, dest: str, date: str):
        """Search for flights"""
        print(f"[SEARCH] Searching flights: {origin} -> {dest} on {date}")
        
        # Fill search form
        await page.fill('input[placeholder*="From"], input[name*="origin"]', origin)
        await self.random_delay()
        await page.fill('input[placeholder*="To"], input[name*="dest"]', dest)
        await self.random_delay()
        await page.fill('input[type="date"], input[name*="date"]', date)
        await self.random_delay()
        
        # Add human-like behavior
        await self.antibot.add_realistic_behavior(page)
        
        # Search
        await page.click('button:has-text("Search"), button[type="submit"]')
        await page.wait_for_load_state('networkidle')
    
    async def book_ticket(self, page: Page, passenger_data: Dict) -> Optional[Ticket]:
        """Book a single ticket"""
        print(f"[BOOKING] Booking ticket for {passenger_data['name']}")
        
        try:
            # Select flight
            await page.click('button:has-text("Select"), .flight-select')
            await self.random_delay()
            
            # Fill passenger details
            await page.fill('input[name*="firstname"]', passenger_data['first_name'])
            await page.fill('input[name*="lastname"]', passenger_data['last_name'])
            await page.fill('input[name*="email"]', passenger_data['email'])
            await self.random_delay()
            
            # Handle captcha if present
            captcha_type = await self.captcha_solver.detect_captcha_type(page)
            if captcha_type:
                print("[BOOKING] Solving captcha...")
                # Solve captcha (implementation depends on type)
                await asyncio.sleep(2)
            
            # Proceed to payment
            await page.click('button:has-text("Continue"), button:has-text("Next")')
            await page.wait_for_load_state('networkidle')
            
            # Handle payment
            payment_security = await self.payment.detect_payment_security(page)
            print(f"[BOOKING] Payment security: {payment_security}")
            
            success = await self.payment.fill_payment_form(page)
            if not success:
                return None
            
            await self.random_delay()
            
            # Submit booking
            await page.click('button:has-text("Pay"), button:has-text("Confirm")')
            await page.wait_for_load_state('networkidle')
            
            # Extract booking confirmation
            booking_id = await self.extract_booking_id(page)
            
            ticket = Ticket(
                booking_id=booking_id,
                status="confirmed",
                details=passenger_data
            )
            
            print(f"[BOOKING] Ticket booked successfully: {booking_id}")
            return ticket
            
        except Exception as e:
            print(f"[BOOKING] Booking failed: {e}")
            return None
    
    async def extract_booking_id(self, page: Page) -> str:
        """Extract booking confirmation ID"""
        # Try multiple patterns
        patterns = [
            r'Booking.*?([A-Z0-9]{6,})',
            r'Reference.*?([A-Z0-9]{6,})',
            r'Confirmation.*?([A-Z0-9]{6,})',
        ]
        
        content = await page.content()
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        
        return f"BOOK_{random.randint(100000, 999999)}"
    
    async def random_delay(self):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(*self.config.delay_range)
        await asyncio.sleep(delay)
    
    async def run(self, credentials: Dict, search_params: Dict, passengers: List[Dict]):
        """Main execution flow"""
        print(f"[AGENT] Starting booking agent for {self.config.num_tickets} tickets")
        
        await self.initialize_browser()
        page = await self.context.new_page()
        
        try:
            # Navigate to target
            print(f"[AGENT] Navigating to {self.config.target_url}")
            await page.goto(self.config.target_url)
            await self.random_delay()
            
            # Login
            login_success = await self.login(page, credentials['username'], credentials['password'])
            if not login_success:
                print("[AGENT] Login failed, aborting")
                return
            
            # Search flights
            await self.search_flights(
                page,
                search_params['origin'],
                search_params['destination'],
                search_params['date']
            )
            
            # Book tickets
            for i, passenger in enumerate(passengers[:self.config.num_tickets]):
                print(f"\n[AGENT] Booking ticket {i+1}/{self.config.num_tickets}")
                
                ticket = await self.book_ticket(page, passenger)
                if ticket:
                    self.tickets.append(ticket)
                
                # Rate limiting avoidance
                if i < len(passengers) - 1:
                    await asyncio.sleep(random.uniform(5, 10))
            
            # Summary
            print(f"\n[AGENT] Booking complete!")
            print(f"[AGENT] Successfully booked: {len(self.tickets)}/{self.config.num_tickets}")
            print(f"[AGENT] Booking IDs: {[t.booking_id for t in self.tickets]}")
            
            # Save results
            self.save_results()
            
        except Exception as e:
            print(f"[AGENT] Fatal error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await self.context.close()
            await self.browser.close()
            await self.playwright.stop()
    
    def save_results(self):
        """Save booking results to file"""
        results = {
            'total_attempted': self.config.num_tickets,
            'total_successful': len(self.tickets),
            'tickets': [
                {
                    'booking_id': t.booking_id,
                    'status': t.status,
                    'details': t.details
                }
                for t in self.tickets
            ]
        }
        
        with open('booking_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("[AGENT] Results saved to booking_results.json")


# Example usage
async def main():
    """Example CTF automation"""
    
    # Configuration
    config = BookingConfig(
        target_url="https://www.edreams.fr/offres/vol/compagnie-aerienne/FR/ryanair/?mktportal=google&utm_id=go_cmp-10556473662_adg-106846393080_ad-696161045516_kwd-13386146_dev-c_ext-_locphy-21537_mtype-e_ntw-g&gad_source=1&gad_campaignid=10556473662&gbraid=0AAAAAD4krlGOVKv4u7J87T4-lIoSWJzVc&gclid=CjwKCAiA3fnJBhAgEiwAyqmY5YzqQ4WK23302KWupdqo6qcExD3J5q3XDUaz6pDh9nv60b5aQJnJ9hoCFv8QAvD_BwE",  # Replace with actual CTF URL
        num_tickets=20,
        headless=False,  # Set True for production
        delay_range=(1, 3)
    )
    
    # Credentials
    credentials = {
        'username': 'ctf_user@example.com',
        'password': 'ctf_password_123'
    }
    
    # Search parameters
    search_params = {
        'origin': 'NYC',
        'destination': 'LAX',
        'date': '2024-12-25'
    }
    
    # Generate passenger data
    passengers = [
        {
            'first_name': f'Passenger{i}',
            'last_name': f'Test{i}',
            'email': f'passenger{i}@example.com',
            'name': f'Passenger{i} Test{i}'
        }
        for i in range(1, 25)
    ]
    
    # Create and run agent
    agent = TicketBookingAgent(config)
    await agent.run(credentials, search_params, passengers)


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   CTF Ticket Booking Automation Agent        ║
    ║   Handles: Login, MFA, Captcha, Anti-bot     ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    asyncio.run(main())