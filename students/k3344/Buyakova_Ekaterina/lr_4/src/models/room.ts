export default interface Room{
  id : number,
  number: number,
  floor: number,
  type: string,
  price_per_day: number,
  phone: string
  is_occupied: boolean
}
