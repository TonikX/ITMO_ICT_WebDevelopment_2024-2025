export interface Owner {
    id: string;
    last_name: string;
    first_name: string;
    patronymic?: string;
    passport_details: string;
    contact_info: string;
    created_at: string;
    updated_at: string;
}

export interface Dog {
    id: string;
    name: string;
    breed: string;
    age: number;
    class_name: string;
    club_name: string;
    owner_id: string;
    owner?: Owner;
    pedigree_document_number: string;
    sire_name: string;
    dam_name: string;
    date_of_last_vaccination: string;
    disqualified: boolean;
    created_at: string;
    updated_at: string;
}

export interface Show {
    id: string;
    name: string;
    date: string;
    type: string;
    location: string;
    sponsor: string;
    ring_schedule: string;
    created_at: string;
    updated_at: string;
}

export interface Participation {
    id: string;
    dog_id: string;
    dog?: Dog;
    show_id: string;
    show?: Show;
    participation_type: string;
    medical_exam_passed: boolean;
    payment_made: boolean;
    medal?: string;
    grades?: Grade[];
    created_at: string;
    updated_at: string;
}

export interface Expert {
    id: string;
    last_name: string;
    first_name: string;
    club_name: string;
    rings_assigned: string;
    created_at: string;
    updated_at: string;
}

export interface Grade {
    id: string;
    participation_id: string;
    participation?: Participation;
    expert_id: string;
    expert?: Expert;
    score: number;
    comment?: string;
    created_at: string;
    updated_at: string;
}

export interface Show {
    id: string;
    name: string;
    date: string;
    type: string;
    location: string;
    sponsor: string;
    ring_schedule: string;
    created_at: string;
    updated_at: string;
}

export interface Expert {
    id: string;
    last_name: string;
    first_name: string;
    club_name: string;
    rings_assigned: string;
    created_at: string;
    updated_at: string;
}
