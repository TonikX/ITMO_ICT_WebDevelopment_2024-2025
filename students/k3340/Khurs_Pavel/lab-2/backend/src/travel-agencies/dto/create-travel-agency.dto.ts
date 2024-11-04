import { IsNotEmpty, IsString } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateTravelAgencyDto {
  @ApiProperty({ example: 'Global Tours' })
  @IsNotEmpty()
  @IsString()
  name: string;

  @ApiProperty({ example: 'contact@globaltours.com' })
  @IsNotEmpty()
  @IsString()
  contactInfo: string;
}
