"""
Seed data utility for populating stages and milestones collections.
Based on PRD Section 5.3 - Real, production-quality content.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path so we can import from backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import connect_to_mongodb, get_database
from models.stage import Stage
from models.milestone import Milestone
from models.resource import Resource


# Stage data - 5 journey stages with next_step_prompt
STAGES_DATA = [
    {
        "title": "Early Signs",
        "description": "Noticing differences and taking the first steps toward understanding your child's unique development.",
        "age_range": "0-3 years",
        "color": "#EAF2F8",
        "icon": "eye",
        "order": 1,
        "next_step_prompt": "When you're ready, you might explore scheduling a developmental screening with your pediatrician."
    },
    {
        "title": "Diagnosis",
        "description": "Navigating evaluations and understanding what a diagnosis means for your family.",
        "age_range": "18 months - 5 years",
        "color": "#E6F2EC",
        "icon": "clipboard",
        "order": 2,
        "next_step_prompt": "When you're ready, you might explore connecting with early intervention services in your area."
    },
    {
        "title": "Early Intervention",
        "description": "Accessing services and building a support team that works for your child.",
        "age_range": "2-5 years",
        "color": "#EDE7F6",
        "icon": "users",
        "order": 3,
        "next_step_prompt": "When you're ready, you might explore learning about educational rights and IEP planning."
    },
    {
        "title": "School Readiness",
        "description": "Preparing for school transitions and understanding educational rights and options.",
        "age_range": "4-8 years",
        "color": "#FFF3E0",
        "icon": "school",
        "order": 4,
        "next_step_prompt": "When you're ready, you might explore building a long-term support network and self-care strategies."
    },
    {
        "title": "Support Resources",
        "description": "Finding community, managing long-term needs, and sustaining your family's wellbeing.",
        "age_range": "All ages",
        "color": "#F2C94C",
        "icon": "heart",
        "order": 5,
        "next_step_prompt": "You're building a strong foundation for your family's journey. Keep celebrating progress and taking care of yourself."
    }
]


# Milestone data - 5-7 simple, observable milestones per stage
MILESTONES_DATA = [
    # Stage 1: Early Signs (S1)
    {
        "stage_id": "S1",
        "title": "My child responds to their name sometimes",
        "behavior": "You've noticed your child occasionally turns or looks when you call their name.",
        "why_it_matters": "Name response is one way children show they're tuned into the world around them. Noticing patterns in when they respond helps you understand what gets their attention.",
        "if_not_yet": "Try calling their name during calm, quiet moments when they're not focused on something else. Some children respond better to certain tones or when you're close by.",
        "reassurance": "Every child develops at their own pace. What matters is that you're paying attention and learning what works for your child."
    },
    {
        "stage_id": "S1",
        "title": "I've written down questions for our pediatrician",
        "behavior": "You've made a list of specific behaviors or concerns to discuss at your next doctor's visit.",
        "why_it_matters": "Writing things down helps you remember what you want to ask and shows your doctor you're observing carefully. It's the first step toward getting answers.",
        "if_not_yet": "Start simple: jot down 2-3 things you've noticed that feel different. You don't need medical terms—just describe what you see.",
        "reassurance": "Asking questions doesn't mean you're overreacting. It means you're being a thoughtful, attentive parent."
    },
    {
        "stage_id": "S1",
        "title": "I'm keeping simple notes about what I notice",
        "behavior": "You're tracking patterns in your child's behavior without obsessing over every detail.",
        "why_it_matters": "Your observations from home are valuable. Simple notes help doctors and specialists understand your child's day-to-day experiences.",
        "if_not_yet": "Keep it easy: note one or two things per week. A sentence or two is enough. You're not building a case—you're just noticing.",
        "reassurance": "You're not overthinking this. You're being thorough, and that helps everyone understand your child better."
    },
    {
        "stage_id": "S1",
        "title": "I've looked at developmental milestone checklists",
        "behavior": "You've reviewed age-appropriate milestones to understand what's typical for your child's age.",
        "why_it_matters": "Understanding milestones gives you context, not a scorecard. It helps you see patterns and have informed conversations with your doctor.",
        "if_not_yet": "Check the CDC's milestone tracker for your child's age. Focus on overall patterns, not individual items. Missing one milestone doesn't define anything.",
        "reassurance": "Learning about milestones is about understanding your child, not finding problems. You're gathering information, and that's smart."
    },
    {
        "stage_id": "S1",
        "title": "I've found one trusted resource that feels helpful",
        "behavior": "You've identified one reliable source of information that doesn't overwhelm you.",
        "why_it_matters": "Having one good resource reduces anxiety and gives you a place to turn when you have questions. Quality over quantity.",
        "if_not_yet": "Try the CDC's 'Learn the Signs, Act Early' program or the Autism Speaks 100 Day Kit. Pick one and stick with it—you don't need to read everything.",
        "reassurance": "One trusted guide is better than endless internet searches. You're being smart about managing information."
    },
    {
        "stage_id": "S1",
        "title": "I'm taking care of myself during this uncertain time",
        "behavior": "You're finding small ways to manage your own stress and emotions.",
        "why_it_matters": "Your wellbeing matters. When you're calmer, you can be more present for your child and make clearer decisions.",
        "if_not_yet": "Identify one small thing that helps you feel better: a walk, talking to a friend, or ten minutes of quiet. Start there.",
        "reassurance": "Taking care of yourself isn't selfish. It's necessary, and it makes you a better parent."
    },
    
    # Stage 2: Diagnosis (S2)
    {
        "stage_id": "S2",
        "title": "I've scheduled a developmental evaluation",
        "behavior": "You've made an appointment with a specialist or early intervention program.",
        "why_it_matters": "Getting on the waitlist is progress, even if the appointment is months away. Early evaluations lead to earlier support.",
        "if_not_yet": "Call your pediatrician for a referral, or contact your state's early intervention program. Making the call is the hardest part.",
        "reassurance": "Seeking an evaluation doesn't mean giving up hope. It means you're taking action to help your child."
    },
    {
        "stage_id": "S2",
        "title": "I understand what happens during evaluations",
        "behavior": "You've learned what to expect so you can prepare yourself and your child.",
        "why_it_matters": "Knowing what's coming reduces anxiety and helps you feel more in control. Most evaluations are play-based and gentle.",
        "if_not_yet": "Ask the evaluation team what the process looks like. Most involve observations, questionnaires, and play activities—nothing scary.",
        "reassurance": "Evaluations are about understanding your child's strengths and needs, not judging them or you."
    },
    {
        "stage_id": "S2",
        "title": "I've gathered notes and videos for the appointment",
        "behavior": "You've prepared examples of behaviors to share with the evaluation team.",
        "why_it_matters": "Your observations from home help evaluators see the full picture. Videos and notes make evaluations more accurate.",
        "if_not_yet": "Bring your notes, any previous screening results, and videos if you have them. Even a few bullet points help.",
        "reassurance": "You're not expected to have everything perfect. Just bring what you have—the team will guide you."
    },
    {
        "stage_id": "S2",
        "title": "I've received evaluation results",
        "behavior": "You've gotten feedback from the evaluation and are processing what it means.",
        "why_it_matters": "A diagnosis is a roadmap, not a limitation. It opens doors to services and helps you understand your child better.",
        "if_not_yet": "If you're waiting for results, know that waiting is often the hardest part. Give yourself grace during this time.",
        "reassurance": "A diagnosis doesn't change who your child is. It just helps you support them better."
    },
    {
        "stage_id": "S2",
        "title": "I've asked questions until I understand",
        "behavior": "You've made sure you understand the diagnosis and what it means for your family.",
        "why_it_matters": "Medical jargon can be confusing. Asking questions ensures you fully understand so you can make informed decisions.",
        "if_not_yet": "Write down questions before appointments: What does this mean day-to-day? What services help? What does the future look like?",
        "reassurance": "Asking questions doesn't mean you're not listening. It means you care enough to truly understand."
    },
    {
        "stage_id": "S2",
        "title": "I've connected with another parent who's been through this",
        "behavior": "You've found at least one parent who can offer perspective and support.",
        "why_it_matters": "Other parents understand what you're going through in ways others may not. Their experiences can light the way forward.",
        "if_not_yet": "Look for local or online parent groups through autism organizations or Facebook. You can just listen at first—that's okay.",
        "reassurance": "You're not alone. Thousands of parents have been exactly where you are, and they're ready to help."
    },
    
    # Stage 3: Early Intervention (S3)
    {
        "stage_id": "S3",
        "title": "I've enrolled in early intervention services",
        "behavior": "You've contacted your state's program or school district to start services.",
        "why_it_matters": "Early intervention services are often free or low-cost and provide therapies tailored to your child's needs. Starting now makes a difference.",
        "if_not_yet": "Google '[your state] early intervention program' or call your school district's special education office. Just make the call.",
        "reassurance": "Starting services doesn't mean your child is behind. It means you're giving them tools to thrive."
    },
    {
        "stage_id": "S3",
        "title": "I understand which therapies my child needs",
        "behavior": "You've learned about different therapy types and what each one addresses.",
        "why_it_matters": "Understanding options helps you make informed decisions. Not every child needs every therapy—focus on your child's specific needs.",
        "if_not_yet": "Ask your evaluation team which therapies they recommend and why. Start with one or two and adjust as you learn.",
        "reassurance": "You don't have to become an expert overnight. Start with what makes sense for your child right now."
    },
    {
        "stage_id": "S3",
        "title": "I've identified key people on our support team",
        "behavior": "You know who your child's main therapists and doctors are and how to reach them.",
        "why_it_matters": "A support team makes the journey less overwhelming. Having trusted people to lean on reduces your stress.",
        "if_not_yet": "Start with your child's primary therapist or case manager. You don't need a huge team—even two or three trusted people help.",
        "reassurance": "You're not expected to do this alone. Building a team is a sign of strength."
    },
    {
        "stage_id": "S3",
        "title": "I understand what my insurance covers",
        "behavior": "You've contacted your insurance to learn about therapy coverage and costs.",
        "why_it_matters": "Understanding coverage reduces financial stress and ensures your child gets consistent services.",
        "if_not_yet": "Call your insurance and ask: What therapies are covered? Do I need pre-authorization? What's my out-of-pocket cost?",
        "reassurance": "Insurance is confusing for everyone. Take it one phone call at a time, and ask for help when you need it."
    },
    {
        "stage_id": "S3",
        "title": "We have consistent daily routines",
        "behavior": "You've built predictable routines that help your child feel secure.",
        "why_it_matters": "Consistent routines reduce anxiety and create natural opportunities to practice skills. Small, consistent changes amplify therapy progress.",
        "if_not_yet": "Start with one routine: morning, mealtime, or bedtime. Use pictures if helpful. Keep it simple—routines should reduce stress.",
        "reassurance": "You don't need a perfect schedule. Even small, consistent routines make a big difference."
    },
    {
        "stage_id": "S3",
        "title": "I'm celebrating small wins",
        "behavior": "You're noticing and celebrating your child's progress, no matter how small.",
        "why_it_matters": "Progress isn't always linear. Celebrating small wins builds momentum and reminds you that your efforts are working.",
        "if_not_yet": "Keep a simple wins journal—jot down one positive thing each week. On hard days, look back and see how far you've come.",
        "reassurance": "Every step forward counts, even the tiny ones. You're doing better than you think."
    },
    
    # Stage 4: School Readiness (S4)
    {
        "stage_id": "S4",
        "title": "I understand my child has educational rights",
        "behavior": "You've learned about IDEA, IEPs, and that your child has legal rights to appropriate education.",
        "why_it_matters": "Federal law guarantees your child the right to free, appropriate education with necessary supports. Knowing this empowers you to advocate.",
        "if_not_yet": "Start with Wrightslaw.com or your state's Parent Training Center. Focus on understanding IEPs first—what they are and how they work.",
        "reassurance": "You don't have to be a legal expert. You just need to know your child's needs matter, and the law supports you."
    },
    {
        "stage_id": "S4",
        "title": "I've requested an IEP evaluation in writing",
        "behavior": "You've formally asked your school district to evaluate your child for special education services.",
        "why_it_matters": "Schools must respond to written requests within specific timeframes. Starting this process early ensures services are ready.",
        "if_not_yet": "Send a simple email: 'I am requesting a full evaluation for special education services for my child, [name], DOB [date].' Keep a copy.",
        "reassurance": "Requesting an evaluation doesn't label your child. It opens doors to support that helps them learn."
    },
    {
        "stage_id": "S4",
        "title": "I'm prepared for the IEP meeting",
        "behavior": "You've gathered information about your child's needs and know what accommodations to request.",
        "why_it_matters": "Preparation helps you advocate confidently. Coming with specific requests ensures your child's needs are clearly addressed.",
        "if_not_yet": "Before the meeting: review reports, list strengths and challenges, identify accommodations you want, and write down questions.",
        "reassurance": "You're not expected to know everything. The team is there to collaborate with you, not test you."
    },
    {
        "stage_id": "S4",
        "title": "I've visited potential classrooms",
        "behavior": "You've toured schools or classrooms to see what might be the best fit.",
        "why_it_matters": "Seeing classrooms helps you understand what supports are available and whether a school feels right for your child.",
        "if_not_yet": "Ask to observe classrooms. Look for: How do teachers handle sensory needs? What's the class size? Does it feel calm or chaotic?",
        "reassurance": "You know your child best. If a placement doesn't feel right, it's okay to ask questions or explore options."
    },
    {
        "stage_id": "S4",
        "title": "I've introduced myself to my child's teacher",
        "behavior": "You've shared key information about your child's needs and established open communication.",
        "why_it_matters": "Teachers are your partners. A strong relationship ensures consistent support and quick problem-solving.",
        "if_not_yet": "Send a brief note introducing your child: their strengths, challenges, what helps them learn, and what triggers stress.",
        "reassurance": "Most teachers genuinely want to help. Starting with collaboration builds a strong foundation."
    },
    {
        "stage_id": "S4",
        "title": "We're preparing for school transitions",
        "behavior": "You're using visual supports, social stories, or practice visits to prepare your child.",
        "why_it_matters": "Preparing in advance reduces anxiety and helps your child adjust more smoothly to new environments.",
        "if_not_yet": "Create a simple visual schedule. Read social stories about school. Visit the classroom before the first day if possible.",
        "reassurance": "Transitions are hard for all kids. Taking time to prepare is thoughtful parenting, not overprotecting."
    },
    
    # Stage 5: Support Resources (S5)
    {
        "stage_id": "S5",
        "title": "I've found my parent community",
        "behavior": "You've connected with other parents of autistic children and feel less alone.",
        "why_it_matters": "Parent communities provide emotional support and practical advice. Shared experiences reduce isolation and build resilience.",
        "if_not_yet": "Look for local support groups through autism organizations or schools. Join online communities where you can ask questions.",
        "reassurance": "Finding your people takes time. Keep looking until you find a community that feels supportive."
    },
    {
        "stage_id": "S5",
        "title": "I'm making time for my own wellbeing",
        "behavior": "You're prioritizing your physical and mental health, recognizing you can't pour from an empty cup.",
        "why_it_matters": "Taking care of yourself isn't selfish—it's essential. Your wellbeing directly impacts your ability to support your child long-term.",
        "if_not_yet": "Identify one small self-care practice: a weekly walk, therapy for yourself, or regular respite care. Start small.",
        "reassurance": "Taking care of yourself makes you a better parent. You deserve support too."
    },
    {
        "stage_id": "S5",
        "title": "I've arranged regular respite care",
        "behavior": "You've identified resources that give you regular breaks to recharge.",
        "why_it_matters": "Respite care prevents burnout and makes you more patient and present. It's not a luxury—it's necessary for sustainable caregiving.",
        "if_not_yet": "Ask your coordinator or insurance about respite services. Many states offer funded respite. Even a few hours a week helps.",
        "reassurance": "Needing a break doesn't mean you're failing. It means you're human."
    },
    {
        "stage_id": "S5",
        "title": "I stay informed without getting overwhelmed",
        "behavior": "You're keeping up with new resources and research without falling into information overload.",
        "why_it_matters": "Staying informed helps you make good decisions, but balance is key. You don't need to know everything.",
        "if_not_yet": "Follow 1-2 trusted sources. Check updates monthly, not daily. Focus on what's relevant to your child's current stage.",
        "reassurance": "You don't have to read everything. Staying informed means being aware, not being overwhelmed."
    },
    {
        "stage_id": "S5",
        "title": "I speak up for my child's needs",
        "behavior": "You're advocating in medical, educational, and community settings to ensure your child's needs are met.",
        "why_it_matters": "Your child needs an advocate, and you're the best person for the job. Your voice makes a real difference.",
        "if_not_yet": "Start small: speak up in one setting where needs aren't being met. Practice what you'll say. Bring documentation if needed.",
        "reassurance": "Advocating for your child isn't pushy. It's necessary, and you're doing it because you love them."
    },
    {
        "stage_id": "S5",
        "title": "I celebrate my child's unique strengths",
        "behavior": "You're embracing your child's strengths, interests, and unique way of experiencing the world.",
        "why_it_matters": "Your child is more than their diagnosis. Celebrating their strengths builds their confidence and reminds you why this journey matters.",
        "if_not_yet": "Make a list of things you love about your child—their humor, creativity, kindness. Share these with them regularly.",
        "reassurance": "Your child is amazing, exactly as they are. Autism is part of their story, not the whole story."
    }
]


# Resource data - ~10 high-quality resources covering all categories
RESOURCES_DATA = [
    {
        "_id": "r1",
        "title": "Autism Speaks: 100 Day Kit",
        "description": "A comprehensive guide for the first 100 days after an autism diagnosis, including practical advice, checklists, and resources for families.",
        "url": "https://www.autismspeaks.org/tool-kit/100-day-kit-young-children",
        "category": "Diagnosis",
        "tags": ["guide", "newly diagnosed", "comprehensive", "family support"]
    },
    {
        "_id": "r2",
        "title": "CDC: Learn the Signs, Act Early",
        "description": "Free developmental milestone checklists and resources to help parents track their child's development and identify early signs of autism.",
        "url": "https://www.cdc.gov/ncbddd/actearly/index.html",
        "category": "Early Intervention",
        "tags": ["milestones", "screening", "early detection", "CDC"]
    },
    {
        "_id": "r3",
        "title": "Wrightslaw: Special Education Law and Advocacy",
        "description": "Comprehensive resource for understanding IDEA, IEPs, 504 plans, and advocating for your child's educational rights.",
        "url": "https://www.wrightslaw.com/",
        "category": "IEP",
        "tags": ["legal rights", "IEP", "advocacy", "education law", "IDEA"]
    },
    {
        "_id": "r4",
        "title": "Insurance Coverage for Autism Services",
        "description": "State-by-state guide to autism insurance mandates, coverage requirements, and how to navigate insurance for therapy services.",
        "url": "https://www.autismspeaks.org/state-initiatives",
        "category": "Insurance",
        "tags": ["insurance", "coverage", "state mandates", "therapy funding"]
    },
    {
        "_id": "r5",
        "title": "Early Intervention: Birth to Three Services",
        "description": "Guide to accessing free or low-cost early intervention services for children under 3, including how to request evaluations and what to expect.",
        "url": "https://www.cdc.gov/ncbddd/actearly/parents/states.html",
        "category": "Early Intervention",
        "tags": ["early intervention", "birth to three", "free services", "evaluations"]
    },
    {
        "_id": "r6",
        "title": "Understanding Applied Behavior Analysis (ABA)",
        "description": "Evidence-based overview of ABA therapy, what it involves, how to find qualified providers, and what research says about effectiveness.",
        "url": "https://www.autismspeaks.org/applied-behavior-analysis-aba-0",
        "category": "Therapy",
        "tags": ["ABA", "therapy", "evidence-based", "behavior"]
    },
    {
        "_id": "r7",
        "title": "Speech and Language Therapy for Autism",
        "description": "Guide to speech therapy approaches for children with autism, including communication strategies and how to support language development at home.",
        "url": "https://www.asha.org/public/speech/disorders/autism/",
        "category": "Therapy",
        "tags": ["speech therapy", "communication", "language development", "ASHA"]
    },
    {
        "_id": "r8",
        "title": "Preparing for Your Child's IEP Meeting",
        "description": "Step-by-step guide to IEP meetings, including what to bring, questions to ask, and how to advocate effectively for your child's needs.",
        "url": "https://www.understood.org/en/articles/preparing-for-an-iep-meeting-a-checklist",
        "category": "IEP",
        "tags": ["IEP meeting", "preparation", "advocacy", "special education"]
    },
    {
        "_id": "r9",
        "title": "Occupational Therapy and Sensory Integration",
        "description": "Overview of occupational therapy for autism, sensory processing challenges, and practical strategies for managing sensory needs.",
        "url": "https://www.aota.org/about/consumers/autism",
        "category": "Therapy",
        "tags": ["occupational therapy", "sensory", "OT", "sensory integration"]
    },
    {
        "_id": "r10",
        "title": "Parent Support and Self-Care Resources",
        "description": "Collection of resources for parent wellbeing, including support groups, respite care options, and strategies for preventing caregiver burnout.",
        "url": "https://www.autismspeaks.org/family-services",
        "category": "General",
        "tags": ["parent support", "self-care", "respite", "mental health", "community"]
    }
]


async def seed_stages():
    """Seed the stages collection with initial data."""
    db = get_database()
    stages_collection = db["stages"]
    
    # Check if stages already exist
    existing_count = await stages_collection.count_documents({})
    if existing_count > 0:
        print(f"⚠ Stages collection already has {existing_count} documents. Skipping seed.")
        return
    
    # Insert stages
    stages = []
    for stage_data in STAGES_DATA:
        stage = Stage(**stage_data)
        stages.append(stage.to_dict())
    
    result = await stages_collection.insert_many(stages)
    print(f"✓ Seeded {len(result.inserted_ids)} stages")


async def seed_milestones():
    """Seed the milestones collection with initial data."""
    db = get_database()
    milestones_collection = db["milestones"]
    
    # Check if milestones already exist
    existing_count = await milestones_collection.count_documents({})
    if existing_count > 0:
        print(f"⚠ Milestones collection already has {existing_count} documents. Skipping seed.")
        return
    
    # Insert milestones
    milestones = []
    for milestone_data in MILESTONES_DATA:
        milestone = Milestone(**milestone_data)
        milestones.append(milestone.to_dict())
    
    result = await milestones_collection.insert_many(milestones)
    print(f"✓ Seeded {len(result.inserted_ids)} milestones")


async def seed_resources():
    """Seed the resources collection with initial data."""
    db = get_database()
    resources_collection = db["resources"]
    
    # Check if resources already exist
    existing_count = await resources_collection.count_documents({})
    if existing_count > 0:
        print(f"⚠ Resources collection already has {existing_count} documents. Skipping seed.")
        return
    
    # Insert resources
    resources = []
    for resource_data in RESOURCES_DATA:
        resource = Resource(**resource_data)
        resources.append(resource.to_dict())
    
    result = await resources_collection.insert_many(resources)
    print(f"✓ Seeded {len(result.inserted_ids)} resources")


async def clear_collections():
    """Clear all collections before re-seeding."""
    db = get_database()
    
    # Clear stages
    stages_result = await db["stages"].delete_many({})
    print(f"✓ Cleared {stages_result.deleted_count} stages")
    
    # Clear milestones
    milestones_result = await db["milestones"].delete_many({})
    print(f"✓ Cleared {milestones_result.deleted_count} milestones")
    
    # Clear resources
    resources_result = await db["resources"].delete_many({})
    print(f"✓ Cleared {resources_result.deleted_count} resources")


async def seed_all():
    """Seed all collections."""
    print("Starting database seeding...")
    
    await connect_to_mongodb()
    
    # Clear existing data
    print("\nClearing existing collections...")
    await clear_collections()
    
    # Seed new data
    print("\nSeeding new data...")
    await seed_stages()
    await seed_milestones()
    await seed_resources()
    
    print("\n✓ Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_all())