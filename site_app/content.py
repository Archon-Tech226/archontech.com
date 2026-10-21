"""Static page content: the four core services and the three default blog posts.

Kept in code (not the database) so it is versioned and reviewable. Blog posts are
copied into the database by `python manage.py seed_blog_posts`, which never
overwrites a post that already exists.
"""

SERVICES = [
    {
        "slug": "web-development",
        "num": "01",
        "name": "Web Development",
        "headline": "Websites built around your business goals",
        "summary": "Responsive business websites that make your offer easy to understand, build trust and guide visitors to an enquiry or purchase.",
        "audience": "Local businesses, freelancers, studios and small companies that need a clear, professional online presence.",
        "need": "People can't find you, can't tell what you offer, or leave before getting in touch.",
        "deliverables": [
            "Business sites, landing pages and portfolios",
            "Product catalogues and simple ecommerce flows where needed",
            "Mobile-first layouts tested on real devices",
            "SEO foundations: titles, headings, clean URLs, alt text",
            "Contact form and analytics set-up",
            "Deployment and agreed maintenance",
        ],
        "process": ["Discuss goals and audience", "Agree pages and content", "Design and review", "Build and test", "Launch and support"],
        "boundaries": "A simple booking or enquiry page is part of a website. A custom booking-management system with accounts, calendars and an admin side is a web application.",
        "faq": [
            ("Will I be able to update it myself?", "That is agreed at the start. We can build it so common changes are simple, or keep updates with us under an agreed arrangement."),
            ("Do you guarantee search rankings?", "No. We build a sound SEO foundation, but rankings depend on many factors and ongoing work."),
        ],
        "cta": "Discuss a website",
        "enquiry": "Website",
        "tags": ["Business sites", "Landing pages", "Portfolios", "Catalogues"],
    },
    {
        "slug": "social-media-marketing",
        "num": "02",
        "name": "Social Media Marketing (SMM)",
        "headline": "Consistent social content with a clear purpose",
        "summary": "Planned, platform-appropriate content, a practical calendar, better profiles and regular performance reviews.",
        "audience": "Businesses that want to stay visible on social platforms but lack the time to plan and post consistently.",
        "need": "Irregular posting, unclear messaging and no view of what is working.",
        "deliverables": [
            "Content strategy and themes",
            "Monthly content calendar",
            "Post and creative design",
            "Scheduling and posting",
            "Profile optimisation",
            "Performance review and reporting",
        ],
        "process": ["Review your profiles and goals", "Agree platforms and themes", "Plan the calendar", "Create and post", "Review and adjust"],
        "boundaries": "This service covers organic content. Paid advertising and ad spend are scoped and budgeted separately so deliverables and costs stay clear.",
        "faq": [
            ("Do you run paid ads?", "Paid campaigns are a separate scope from organic content, with ad spend paid directly to the platform. Ask us if you want to explore it."),
            ("Can I take social media without a website?", "Yes. Each service can be taken on its own."),
        ],
        "cta": "Plan my social media",
        "enquiry": "Social media marketing",
        "tags": ["Content calendar", "Post design", "Profile set-up", "Reporting"],
    },
    {
        "slug": "web-applications",
        "num": "03",
        "name": "Web Applications",
        "headline": "Custom workflows, not just static pages",
        "summary": "Database-backed applications for the workflows your business runs on: enquiries, bookings, billing, dashboards and portals.",
        "audience": "Businesses whose work is held together by spreadsheets, paper or repeated manual steps.",
        "need": "Data scattered across tools, slow manual processes, and no single place for the team.",
        "deliverables": [
            "Requirements and a defined first version (MVP)",
            "Database-backed workflows and forms",
            "Dashboards and role-based access",
            "Integrations that are agreed in scope",
            "Testing and deployment",
            "Handover and post-launch fixes",
        ],
        "process": ["Map the workflow", "Define the MVP", "Design key screens", "Build and test with you", "Deploy and support"],
        "boundaries": "We start from a defined MVP. Extra modules and integrations are added in later, separately agreed phases.",
        "faq": [
            ("How is this different from a website?", "A website mostly informs. A web application stores data, has logins and supports a workflow your team uses day to day."),
            ("Can you build on what I already use?", "Often, yes. We look at your current process first and propose the simplest approach that fits."),
        ],
        "cta": "Discuss an application",
        "enquiry": "Web application",
        "tags": ["Dashboards", "Role-based access", "Booking tools", "Internal tools"],
    },
    {
        "slug": "saas-products",
        "num": "04",
        "name": "SaaS Products",
        "headline": "Turn a useful idea into a usable product",
        "summary": "We help shape and build SaaS MVPs with a clear first-use experience, accounts, core workflows and admin controls.",
        "audience": "Founders and teams with a product idea that serves many customers and needs a first working version.",
        "need": "An idea that needs scoping, a first usable version and a path to improve it.",
        "deliverables": [
            "Discovery and MVP scoping",
            "User accounts and sign-in",
            "Core workflow that delivers the main value",
            "Admin controls",
            "Roadmap for later improvements",
            "Deployment of the first version",
        ],
        "process": ["Discovery", "Scope the MVP", "Design the first-use flow", "Build and test", "Launch and iterate"],
        "boundaries": "Subscription billing, third-party integrations, analytics and advanced features are included only when agreed in scope.",
        "faq": [
            ("What is the difference between a web app and SaaS?", "A web application can serve one business. A SaaS product serves many separate customers from one system, which adds accounts, data separation and ongoing maintenance."),
            ("Do you build the full product at once?", "We recommend a focused MVP first, then improve it based on real use."),
        ],
        "cta": "Explore a SaaS MVP",
        "enquiry": "SaaS product",
        "tags": ["MVP scoping", "Accounts", "Admin controls", "Roadmap"],
    },
]

PROCESS_STEPS = [
    ("Discuss", "We learn what your business needs and agree what to build."),
    ("Design", "You see the layout and flow before any code is written."),
    ("Build", "We develop it, share progress and test on real devices."),
    ("Launch and support", "We put it live and stay available for fixes and updates."),
]

# Body format: '## ' heading, '- ' bullet, blank line between paragraphs.
BLOG_POSTS = [
    {
        "slug": "small-business-website-launch-checklist",
        "title": "What Should a Small Business Website Include Before Launch?",
        "category": "Websites",
        "excerpt": "A practical pre-launch checklist for small business websites, from the offer and contact path to performance, accessibility and maintenance.",
        "body": """A launch is easier when you know what "finished" looks like. This checklist covers what most small business websites should have in place before going live. Your needs will vary by business, so treat it as a starting point rather than a rulebook.

## Say what you offer, clearly
- A headline that explains what you do and who it is for
- Your main services or products, described in plain language
- One clear next step, such as call, message or request a quote

## Show genuine trust evidence
- Real photos, real project examples and accurate business details
- Genuine, approved customer feedback if you have it
- Leave out anything you cannot back up, such as invented numbers or awards

## Work well on a phone
- Text that is readable without zooming
- Buttons large enough to tap
- Menus that open and close reliably

## Make contact easy
- A working contact form, phone number or WhatsApp link
- Test the form yourself and confirm you receive the message
- Say what happens after someone gets in touch

## Check speed and accessibility
- Compress images and avoid oversized files
- Sufficient colour contrast and descriptive image alt text
- Pages that can be used with a keyboard

## Cover privacy and legal basics where relevant
- A privacy note if you collect personal details
- Any business information required where you operate

## Set up analytics and maintenance
- Basic analytics so you can see what visitors do
- A plan for who updates content and who fixes problems

## Quick pre-launch checklist
- Every page and link tested
- Contact form tested end to end
- Mobile and desktop checked
- Titles and descriptions written for each page
- Backups and a maintenance contact agreed

If you would like a second pair of eyes on your plan, Archon Tech can review your website plan with you.""",
        "cta_label": "Ask Archon Tech to review your website plan",
        "cta_service": "Website",
    },
    {
        "slug": "local-business-website-seo-basics",
        "title": "Website SEO Basics for Local Businesses",
        "category": "SEO",
        "excerpt": "The on-page SEO fundamentals a local business website should get right, without promises about rankings.",
        "body": """Search engine optimisation (SEO) is the practice of making your site easier for people and search engines to understand. These basics are a solid foundation. No one can guarantee rankings, and results vary and take ongoing work.

## Write clear page titles
Each page should have a unique title that says what the page is about, for example the service and the place you serve. Keep it readable rather than stuffed with keywords.

## Use headings properly
- One main heading per page that describes its topic
- Subheadings that break the content into logical parts
- Headings written for people first

## Keep URLs descriptive
A URL such as /services/web-development tells visitors and search engines more than /page?id=7. Keep them short and consistent.

## Describe your images
- Add alt text that describes what the image shows
- Compress images so pages load quickly
- Avoid putting important text only inside an image

## Make the site fast on mobile
Many local searches happen on phones. Check that pages load promptly, text is readable and buttons are easy to tap.

## Link your pages together
Link from one relevant page to another, such as from a service page to the contact page. This helps visitors find their way and helps search engines understand your site.

## Keep business details accurate
- Name, address and phone number consistent across your site and profiles
- Opening hours kept up to date
- Only claim service areas you actually serve

## Publish useful service and location content
Explain what you do, who it helps and where you work, in your own words. Helpful, accurate pages tend to serve both visitors and search engines better than thin or copied text.

## Be realistic
SEO builds over time and depends on many factors outside your site. A good foundation helps, but it is not a guarantee.

If you want your site built with these foundations in place, Archon Tech can discuss an SEO-ready website foundation with you.""",
        "cta_label": "Discuss an SEO-ready website foundation",
        "cta_service": "Website",
    },
    {
        "slug": "website-vs-web-application-vs-saas",
        "title": "Website vs Web Application vs SaaS: What Does Your Business Need?",
        "category": "Planning",
        "excerpt": "Three things often get mixed up. Here is how a website, a web application and a SaaS product differ, and the questions that help you choose.",
        "body": """People often use "website", "web app" and "SaaS" as if they mean the same thing. They solve different problems, and choosing the right starting point can save time and money.

## A public marketing website
A website presents your business to visitors: what you offer, examples of your work and how to get in touch. Visitors usually do not need to log in. It is the right start if your main goal is to be found and trusted.

## A workflow-oriented web application
A web application helps a team or its customers do something: manage bookings, track enquiries, create bills or view a dashboard. It stores data, usually has logins and different roles, and supports a process you repeat. It is the right choice when your work currently runs on spreadsheets, paper or repeated manual steps.

## A multi-customer SaaS product
SaaS (software as a service) is a product that many separate customers use, each with their own account and data, usually on an ongoing basis. It involves extra considerations such as data separation, onboarding and long-term maintenance. It is the right path if you want to offer software itself as your product.

## Questions that help you decide
- Who will use it: visitors, your team, your customers, or many businesses?
- Does anyone need to log in?
- Does it need to save data or support a workflow?
- Will multiple separate customers each need their own space?
- Who will maintain and improve it over time?

## A sensible way to start
Many projects begin with a website, add a web application when a workflow needs it, and only become a SaaS product once there is a clear need from multiple customers. Starting with the smallest useful version lets you learn before investing more.

If you are unsure where you fall, tell us what you are trying to do and we will help you work out a sensible starting scope.""",
        "cta_label": "Discuss the right starting scope with Archon Tech",
        "cta_service": "Not sure yet",
    },
]

SAMPLE_TESTIMONIALS = [
    ("Sample Client A", "Sample company", "SAMPLE ONLY: replace this with a genuine, approved client quote before launch."),
    ("Sample Client B", "Sample company", "SAMPLE ONLY: this placeholder must never be shown as a real endorsement."),
    ("Sample Client C", "Sample company", "SAMPLE ONLY: delete or replace this entry from the dashboard."),
]
