export interface Distribution {
    id: string;
    newspaper: {
        id: string;
        name: string;
    };
    printshop: {
        id: string;
        name: string;
        address: string;
    };
    postoffice: {
        id: string;
        office_number: number;
        address: string;
    };
    copies_printed: number;
    copies_sent: number;
    created_at: string;
    updated_at: string;

}
