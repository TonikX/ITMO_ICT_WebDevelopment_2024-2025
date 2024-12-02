import {ApiProperty} from "@nestjs/swagger";
import {LoginArtistDto} from "./login-artist.dto";
import {IsString, Length} from "class-validator";

export class CreateArtistDto extends LoginArtistDto {
    @ApiProperty({example: 'Riley Parker'})
    @IsString({message: 'Name must be string'})
    @Length(1, 50, {message: 'Name length must be between 1 and 50'})
    readonly name: string;
}