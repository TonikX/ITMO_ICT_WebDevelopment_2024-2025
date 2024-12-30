import {ApiProperty} from "@nestjs/swagger";
import {IsString, Length} from "class-validator";

export class LoginArtistDto {
    @ApiProperty({example: 'rileyparker'})
    @IsString({message: 'Username must be string'})
    @Length(6, 20, {message: 'Username length must be between 6 and 20'})
    readonly username: string;

    @ApiProperty({example: 'password123'})
    @IsString({message: 'Password must be string'})
    @Length(4, 22, {message: 'Password length must be between 4 and 22'})
    readonly password: string;
}