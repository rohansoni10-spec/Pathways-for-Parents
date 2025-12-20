export interface Stage {
  id: string;
  title: string;
  description: string;
  ageRange: string;
  color: string;
  icon: string;
}

export interface Milestone {
  id: string;
  stageId: string;
  title: string;
  behavior: string;
  whyItMatters: string;
  ifNotYet: string;
  reassurance: string;
}

export interface Resource {
  id: string;
  title: string;
  description: string;
  url: string;
  category: 'Early Intervention' | 'Diagnosis' | 'Insurance' | 'IEP' | 'Therapy' | 'General';
  tags: string[];
}

export const STAGES: Stage[] = [
  {
    id: 's1',
    title: 'Early Signs',
    description: 'Noticing differences and wondering what they mean.',
    ageRange: '0-3 years',
    color: 'bg-amber-100 text-amber-800',
    icon: 'Eye'
  },
  {
    id: 's2',
    title: 'Diagnosis',
    description: 'Navigating evaluations and understanding the results.',
    ageRange: '18mo - 5 years',
    color: 'bg-purple-100 text-purple-800',
    icon: 'Stethoscope'
  },
  {
    id: 's3',
    title: 'Early Intervention',
    description: 'Starting therapies and support services.',
    ageRange: '0-3 years',
    color: 'bg-emerald-100 text-emerald-800',
    icon: 'Sprout'
  },
  {
    id: 's4',
    title: 'School Readiness',
    description: 'Transitioning to school and setting up IEPs.',
    ageRange: '3-6 years',
    color: 'bg-blue-100 text-blue-800',
    icon: 'School'
  },
  {
    id: 's5',
    title: 'Support Resources',
    description: 'Finding community and sustaining yourself.',
    ageRange: 'All ages',
    color: 'bg-rose-100 text-rose-800',
    icon: 'Heart'
  }
];

export const MILESTONES: Milestone[] = [
  // Stage 1: Early Signs
  {
    id: 'm1-1',
    stageId: 's1',
    title: 'Observe Eye Contact',
    behavior: 'Notice if your child looks at you when you call their name or smile at them.',
    whyItMatters: 'Eye contact is a key way children connect and share attention. It helps them learn from others.',
    ifNotYet: 'Try getting down to their eye level. Hold a favorite toy near your face to encourage looking towards you.',
    reassurance: 'Many children have varying levels of eye contact. It can improve with gentle encouragement.'
  },
  {
    id: 'm1-2',
    stageId: 's1',
    title: 'Track Gestures',
    behavior: 'Look for pointing, waving, or reaching to show you things.',
    whyItMatters: 'Gestures are often the bridge to spoken language. They show a desire to communicate.',
    ifNotYet: 'Model gestures for them. Wave "bye-bye" exaggeratedly. Point to things you see on a walk.',
    reassurance: 'Some children rely more on leading you by hand than pointing. That is still communication.'
  },
  {
    id: 'm1-3',
    stageId: 's1',
    title: 'Response to Name',
    behavior: 'Check if your child turns or pauses when you say their name.',
    whyItMatters: 'Responding to their name shows they are tuning into social signals.',
    ifNotYet: 'Touch their shoulder gently while saying their name. Make it a game with tickles or treats.',
    reassurance: 'They might be hyper-focused on play. It doesn’t always mean they can’t hear or ignore you.'
  },
  
  // Stage 2: Diagnosis
  {
    id: 'm2-1',
    stageId: 's2',
    title: 'Schedule Evaluation',
    behavior: 'Contact your pediatrician or a local specialist to request a developmental evaluation.',
    whyItMatters: 'Waitlists can be long. Getting on the list is the most important first step.',
    ifNotYet: 'If you are hesitant, remember: an evaluation is just information. It opens doors to support.',
    reassurance: 'You are being proactive. That is the best thing you can do for your child.'
  },
  {
    id: 'm2-2',
    stageId: 's2',
    title: 'Document Behaviors',
    behavior: 'Keep a simple log of behaviors that concern you or things your child does well.',
    whyItMatters: 'Doctors only see a snapshot. Your notes help them see the full picture.',
    ifNotYet: 'Just jot down 3 things you noticed today in a notebook or phone app.',
    reassurance: 'You know your child best. Your observations are valid and valuable.'
  },
  {
    id: 'm2-3',
    stageId: 's2',
    title: 'Understand the Report',
    behavior: 'Read through the evaluation report and highlight terms you don’t know.',
    whyItMatters: 'The report is the key to getting services. Understanding it empowers you to advocate.',
    ifNotYet: 'Ask the evaluator to explain the summary section in plain language.',
    reassurance: 'The diagnosis describes behaviors, it doesn’t change who your child is.'
  },

  // Stage 3: Early Intervention
  {
    id: 'm3-1',
    stageId: 's3',
    title: 'Contact Early Intervention',
    behavior: 'Call your state’s Early Intervention (EI) program for a free assessment (if under 3).',
    whyItMatters: 'EI is federally mandated and often free. It brings therapy to your home.',
    ifNotYet: 'Search "[Your State] Early Intervention" to find the number.',
    reassurance: 'You don’t need a doctor’s referral in most states to get started.'
  },
  {
    id: 'm3-2',
    stageId: 's3',
    title: 'Set One Goal',
    behavior: 'Pick one specific thing you want to work on (e.g., "sitting for 2 minutes").',
    whyItMatters: 'Focusing on everything at once is overwhelming. Small wins build momentum.',
    ifNotYet: 'Think about what would make your daily life 1% easier right now.',
    reassurance: 'Progress is not linear. Celebrating small steps keeps you going.'
  },
  {
    id: 'm3-3',
    stageId: 's3',
    title: 'Create a Routine',
    behavior: 'Establish a simple visual schedule or consistent routine for morning/bedtime.',
    whyItMatters: 'Predictability reduces anxiety for many children on the spectrum.',
    ifNotYet: 'Start with just "First bath, then book" pictures.',
    reassurance: 'It doesn’t have to be perfect. Consistency helps more than complexity.'
  },

  // Stage 4: School Readiness
  {
    id: 'm4-1',
    stageId: 's4',
    title: 'Request IEP Meeting',
    behavior: 'Send a written request to your school district for an IEP evaluation.',
    whyItMatters: 'An IEP (Individualized Education Program) is a legal document ensuring support.',
    ifNotYet: 'Use a template letter found online to make it formal.',
    reassurance: 'You are an equal member of the IEP team. Your voice matters.'
  },
  {
    id: 'm4-2',
    stageId: 's4',
    title: 'Visit the School',
    behavior: 'Ask to tour the classroom or meet the teacher before school starts.',
    whyItMatters: 'Familiarity reduces fear. Seeing the space helps you prepare your child.',
    ifNotYet: 'Look at pictures of the school online with your child.',
    reassurance: 'Teachers want to help. They appreciate your involvement.'
  },
  {
    id: 'm4-3',
    stageId: 's4',
    title: 'Practice Self-Help',
    behavior: 'Work on simple skills like putting on a backpack or opening a lunchbox.',
    whyItMatters: 'Independence in small tasks boosts confidence in the classroom.',
    ifNotYet: 'Make it a game at home. "Race" to zip up the jacket.',
    reassurance: 'They don’t need to do it perfectly. Trying is the first step.'
  },

  // Stage 5: Support Resources
  {
    id: 'm5-1',
    stageId: 's5',
    title: 'Find a Community',
    behavior: 'Join a local support group or a moderated online community.',
    whyItMatters: 'Talking to parents who "get it" is the best stress reliever.',
    ifNotYet: 'Look for Facebook groups for "Autism parents in [Your City]".',
    reassurance: 'You are not alone. There is a whole village waiting for you.'
  },
  {
    id: 'm5-2',
    stageId: 's5',
    title: 'Apply for Respite',
    behavior: 'Look into respite care funding or ask a trusted family member for a break.',
    whyItMatters: 'Caregiver burnout is real. You need rest to be the best parent you can be.',
    ifNotYet: 'Start with just 1 hour for yourself to have coffee or nap.',
    reassurance: 'Taking a break is not selfish. It is essential maintenance.'
  },
  {
    id: 'm5-3',
    stageId: 's5',
    title: 'Explore Financial Aid',
    behavior: 'Research grants, waivers, or insurance benefits for autism therapies.',
    whyItMatters: 'Therapy is expensive. There are often hidden funds available.',
    ifNotYet: 'Ask your therapist or social worker if they know of any grants.',
    reassurance: 'It takes time to navigate, but the financial relief is worth it.'
  }
];

export const RESOURCES: Resource[] = [
  {
    id: 'r1',
    title: 'Autism Speaks: 100 Day Kit',
    description: 'A comprehensive guide for the first 100 days after an autism diagnosis.',
    url: 'https://www.autismspeaks.org/tool-kit/100-day-kit-young-children',
    category: 'Diagnosis',
    tags: ['guide', 'newly diagnosed']
  },
  {
    id: 'r2',
    title: 'Wrightslaw: Special Education Law',
    description: 'The go-to source for accurate, reliable information about special education law and advocacy.',
    url: 'https://www.wrightslaw.com/',
    category: 'IEP',
    tags: ['legal', 'advocacy', 'school']
  },
  {
    id: 'r3',
    title: 'CDC: Milestones in Action',
    description: 'Photos and videos of developmental milestones to help you know what to look for.',
    url: 'https://www.cdc.gov/ncbddd/actearly/milestones/index.html',
    category: 'Early Intervention',
    tags: ['development', 'official']
  },
  {
    id: 'r4',
    title: 'Understood.org',
    description: 'Resources for learning and thinking differences, including practical tips for parents.',
    url: 'https://www.understood.org/',
    category: 'General',
    tags: ['tips', 'behavior']
  },
  {
    id: 'r5',
    title: 'Medicaid Waiver Information',
    description: 'Guide to understanding Home and Community Based Services (HCBS) waivers.',
    url: 'https://www.medicaid.gov/medicaid/home-community-based-services/index.html',
    category: 'Insurance',
    tags: ['financial', 'government']
  },
  {
    id: 'r6',
    title: 'Hanen Centre: Tips for Parents',
    description: 'Practical strategies for building communication skills in everyday situations.',
    url: 'http://www.hanen.org/Helpful-Info/Parent-Tips.aspx',
    category: 'Therapy',
    tags: ['speech', 'communication']
  }
];
