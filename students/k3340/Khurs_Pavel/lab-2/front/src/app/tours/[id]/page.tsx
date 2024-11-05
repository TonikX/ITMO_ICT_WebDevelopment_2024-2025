import MainTourCard from "@/app/tours/[id]/components/MainCard";
import { reviewsService } from "@/services/reviewService";
import { toursService } from "@/services/tourService";

type Props = {
  params: Promise<{ id: string }>;
};
export default async function Page(props: Props) {
  const params = await props.params;

  const tourData = await toursService.getTourById(params.id);
  const reviewsData = await reviewsService.getAllReviews(params.id);

  return (
    <div className="flex flex-wrap gap-8 container mx-auto">
      <MainTourCard tourData={tourData} reviews={reviewsData} />
    </div>
  );
}
