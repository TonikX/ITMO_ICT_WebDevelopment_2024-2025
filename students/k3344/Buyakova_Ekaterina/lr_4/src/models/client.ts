export default interface Client{
  id: number,
  passport_number: string,
  last_name: string,
  first_name: string,
  city: string,
  room_number: number | null
}
