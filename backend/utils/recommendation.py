from models.onboarding import ChildAgeRange, DiagnosisStatus, PrimaryConcern


def calculate_recommended_stage(
    age_range: ChildAgeRange,
    diagnosis_status: DiagnosisStatus,
    primary_concern: PrimaryConcern
) -> str:
    """
    Calculate the recommended journey stage based on onboarding responses.
    
    Logic:
    1. Diagnosis Status (Base):
       - "none" -> "s1"
       - "waiting" -> "s2"
       - "recent" (<=12mo) -> "s3"
       - "established" (>12mo) -> "s4"
    
    2. Age Guardrails (Cap):
       - "0-18m" -> max "s1"
       - "18-36m" -> max "s2"
       - "3-5y" -> max "s3"
       - "5-8y" -> max "s4"
       Rule: If base > max, use max.
    
    3. Concern Overrides:
       - Concern="school" AND Age="5-8y" -> "s4"
       - Concern="speech" AND Age < 3y ("0-18m" or "18-36m") -> "s1"
       - Concern="behavior" AND Diagnosis="recent" -> "s3"
    
    Args:
        age_range: Child's age range
        diagnosis_status: Current diagnosis status
        primary_concern: Primary concern area
    
    Returns:
        str: Recommended stage ID ("s1", "s2", "s3", or "s4")
    """
    
    # Step 1: Determine base stage from diagnosis status
    diagnosis_to_stage = {
        DiagnosisStatus.NONE: "s1",
        DiagnosisStatus.WAITING: "s2",
        DiagnosisStatus.RECENT: "s3",
        DiagnosisStatus.ESTABLISHED: "s4"
    }
    base_stage = diagnosis_to_stage[diagnosis_status]
    
    # Step 2: Apply age guardrails (cap)
    age_to_max_stage = {
        ChildAgeRange.AGE_0_18M: "s1",
        ChildAgeRange.AGE_18_36M: "s2",
        ChildAgeRange.AGE_3_5Y: "s3",
        ChildAgeRange.AGE_5_8Y: "s4"
    }
    max_stage = age_to_max_stage[age_range]
    
    # Apply cap: if base > max, use max
    stage_order = ["s1", "s2", "s3", "s4"]
    if stage_order.index(base_stage) > stage_order.index(max_stage):
        recommended_stage = max_stage
    else:
        recommended_stage = base_stage
    
    # Step 3: Apply concern overrides
    # Override 1: Concern="school" AND Age="5-8y" -> "s4"
    if primary_concern == PrimaryConcern.SCHOOL and age_range == ChildAgeRange.AGE_5_8Y:
        recommended_stage = "s4"
    
    # Override 2: Concern="speech" AND Age < 3y -> "s1"
    if primary_concern == PrimaryConcern.SPEECH and age_range in [
        ChildAgeRange.AGE_0_18M,
        ChildAgeRange.AGE_18_36M
    ]:
        recommended_stage = "s1"
    
    # Override 3: Concern="behavior" AND Diagnosis="recent" -> "s3"
    if primary_concern == PrimaryConcern.BEHAVIOR and diagnosis_status == DiagnosisStatus.RECENT:
        recommended_stage = "s3"
    
    return recommended_stage