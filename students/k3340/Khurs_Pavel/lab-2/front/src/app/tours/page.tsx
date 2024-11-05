import { TourData } from "@/app/tours/types";
import TourCard from "@/components/TourCard";
import { toursService } from "@/services/tourService";

export default async function Page() {
  const data = await toursService.getAllTours();
  console.log(data);

  return (
    <div className="flex flex-wrap gap-8 container mx-auto">
      {data.map((item: TourData) => {
        return <TourCard key={item.id.toString()} {...item} />;
      })}
    </div>
  );
}
