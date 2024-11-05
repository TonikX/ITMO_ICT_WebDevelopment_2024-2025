"use client";
import Image from "next/image";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  Input,
  Textarea,
} from "@nextui-org/react";
import { useState } from "react";
import { ReviewData, TourData } from "@/app/tours/types";
import toast from "react-hot-toast";

interface MainTourCardProps {
  tourData: TourData;
  reviews?: ReviewData[];
}

const MainTourCard: React.FC<MainTourCardProps> = ({ tourData, reviews }) => {
  const [reviewList, setReviewList] = useState<ReviewData[]>(reviews || []);
  const [newReview, setNewReview] = useState({
    comment: "",
    rating: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const averageRating = reviewList.length
    ? (
        reviewList.reduce((sum, review) => sum + review.rating, 0) /
        reviewList.length
      ).toFixed(1)
    : "N/A";

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setNewReview((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const submitReview = async () => {
    if (!newReview.comment || !newReview.rating) {
      toast.error("Пожалуйста заполните все поля");
      return;
    }

    setIsSubmitting(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/reviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          tourId: tourData.id,
          comment: newReview.comment,
          rating: Number(newReview.rating),
        }),
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.message);
      }

      const addedReview: ReviewData = await res.json();
      setReviewList((prev) => [addedReview, ...prev]);
      setNewReview({ comment: "", rating: "" });
    } catch (error) {
      toast(error as string);
    } finally {
      setIsSubmitting(false);
    }
  };
  const createBooking = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/reservations`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            tourId: tourData.id,
          }),
        }
      );

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.message);
      }
      toast("Вы успешно забронировали тур!!!");
    } catch (error) {
      toast(error as string);
    } finally {
    }
  };
  return (
    <div className="min-w-full p-4 h-full max-h-screen my-auto">
      <Card className="w-full shadow-2xl overflow-hidden flex flex-row max-h-fill">
        <div className="flex-1 justify-between">
          <CardHeader className="p-0">
            <Image
              className="w-full h-64 object-cover"
              src="https://images.unsplash.com/photo-1540206395-68808572332f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
              alt={tourData.title}
              height={256}
              width={256}
            />
          </CardHeader>
          <CardBody className="p-6">
            <span className="block text-2xl font-bold mb-2">
              {tourData.title}
            </span>
            <span className="block mb-4">{tourData.description}</span>
            <div className="flex items-center mb-4">
              <svg
                className="h-5 w-5 text-yellow-500 mr-1"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
              </svg>
              <span className=" ml-1">
                {averageRating} ({reviewList.length} reviews)
              </span>
            </div>
          </CardBody>
          <CardFooter className="flex justify-between items-center">
            <span className="text-2xl font-bold ">
              Предоплата {tourData.paymentConditions}
            </span>
            <Button color="primary" onClick={createBooking}>
              Забронировать
            </Button>
          </CardFooter>
        </div>
        <div className="w-1/3 p-4 flex justify-between flex-col max-h-[488px]">
          <div className="overflow-y-auto">
            <span className="block text-lg font-semibold mb-2">Отзывы</span>
            <div className="space-y-2">
              {reviewList.map((review, index) => (
                <Card key={index} className="p-3 flex flex-row justify-between">
                  <div className="">
                    <span className="block font-medium ">
                      {review.user.email}
                    </span>
                    <span className="block text-sm ">{review.comment}</span>
                  </div>
                  <div className="flex items-center">
                    <span>Оценка</span>
                    <span className=" ml-1">{review.rating}</span>
                  </div>
                </Card>
              ))}
            </div>
          </div>
          <div className="mt-7">
            <span className="block text-lg font-semibold mb-2">
              Добавить отзыв
            </span>
            <div className="mb-4">
              <Textarea
                name="comment"
                placeholder="Ваш комментарий"
                value={newReview.comment}
                onChange={handleInputChange}
                className="mb-2"
              />
              <Input
                name="rating"
                type="number"
                placeholder="Оценка (1-10)"
                value={newReview.rating}
                onChange={handleInputChange}
                min={1}
                max={10}
              />
              <Button
                onPress={submitReview}
                color="success"
                isDisabled={isSubmitting}
                className="relative -bottom-5"
              >
                {isSubmitting ? "Отправка..." : "Добавить отзыв"}
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default MainTourCard;
