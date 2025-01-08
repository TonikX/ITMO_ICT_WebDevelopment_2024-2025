import {ApiProperty, OmitType, PartialType} from "@nestjs/swagger";
import {IsOptional, IsString, Length} from "class-validator";
import {CreateArtistDto} from "./create-artist.dto";

export class UpdateArtistDto extends PartialType(OmitType(CreateArtistDto, ['password'] as const)) {
    @ApiProperty({example: 'Artist profile desc :)'})
    @IsOptional()
    @IsString({message: 'Description must be string'})
    @Length(0, 140, {message: 'Description length must be less then 140'})
    readonly description?: string;
}